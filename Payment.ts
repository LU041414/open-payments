import dotenv from "dotenv";
import {
  type WalletAddress,
  type AuthenticatedClient,
  type Grant,
  createAuthenticatedClient,
  type PendingGrant,
  isPendingGrant,
} from "@interledger/open-payments";
import { randomUUID } from "crypto";
import { type components } from "@interledger/open-payments/dist/openapi/generated/auth-server-types";

export async function automateInterledgerTransaction(
  client: AuthenticatedClient,
  input: {
    senderWalletAddress: string; // user-provided
    receiverWalletAddress: string; // environment/client's own address
    amount: string; // incoming payment amount
    redirectUrl: string; // used for OP authorization
    type?: "new_subscription";
    payments?: number;
    duration?: string;
  }
) {
  // Normalize addresses
  const senderAddress = normalizeWalletAddress(input.senderWalletAddress);
  const receiverAddress = normalizeWalletAddress(input.receiverWalletAddress);

  // Step 1: Get Wallet Info
  const {
    walletAddressDetails: receiverDetails
  } = await getWalletAddressInfo(client, receiverAddress);

  const {
    walletAddressDetails: senderDetails
  } = await getWalletAddressInfo(client, senderAddress);

  // Step 2: Create Incoming Payment (Receiver)
  const ipGrant = await client.grant.request(
    {
      url: receiverDetails.authServer,
    },
    {
      access_token: {
        access: [
          {
            type: "incoming-payment",
            actions: ["read", "create", "complete"],
          },
        ],
      },
    }
  );
  if (isPendingGrant(ipGrant)) throw new Error("Expected non-interactive grant");

  const incomingPayment = await client.incomingPayment.create(
    {
      url: receiverDetails.resourceServer,
      accessToken: ipGrant.access_token.value,
    },
    {
      walletAddress: receiverDetails.id,
      incomingAmount: {
        value: input.amount,
        assetCode: receiverDetails.assetCode,
        assetScale: receiverDetails.assetScale,
      },
      expiresAt: new Date(Date.now() + 60 * 30 * 1000).toISOString(), // 30 mins
    }
  );
  console.log("Incoming Payment Created:", incomingPayment.id);

  // Step 3: Create Quote (Sender → Receiver)
  const quoteGrant = await client.grant.request(
    {
      url: senderDetails.authServer,
    },
    {
      access_token: {
        access: [
          {
            type: "quote",
            actions: ["create", "read", "read-all"],
          },
        ],
      },
    }
  );
  if (isPendingGrant(quoteGrant)) throw new Error("Expected non-interactive quote grant");

  const quote = await client.quote.create(
    {
      url: senderDetails.resourceServer,
      accessToken: quoteGrant.access_token.value,
    },
    {
      method: "ilp",
      walletAddress: senderDetails.id,
      receiver: incomingPayment.id,
    }
  );
  console.log("Quote Created:", quote.id);

  // Step 4: Request Outgoing Payment Pending Grant
  const now = new Date().toISOString();
  const opPendingGrant = await client.grant.request(
    {
      url: senderDetails.authServer,
    },
    {
      access_token: {
        access: [
          {
            identifier: senderDetails.id,
            type: "outgoing-payment",
            actions: ["list", "list-all", "read", "read-all", "create"],
            limits: {
              debitAmount: quote.debitAmount,
              receiveAmount: quote.receiveAmount,
              ...(input.type === "new_subscription"
                ? {
                    interval: `R${input.payments}/${now}/${
                      input.duration ?? "PT10M"
                    }`,
                  }
                : {}),
            },
          },
        ],
      },
      interact: {
        start: ["redirect"],
        finish: {
          method: "redirect",
          uri: input.redirectUrl,
          nonce: randomUUID(),
        },
      },
    }
  );
  if (!isPendingGrant(opPendingGrant)) {
    throw new Error("Expected interactive outgoing-payment grant.");
  }

  console.log("Pending Grant - Authorization Required:");
  console.log(opPendingGrant.interact.redirect);
  console.log("Save to continue later:");
  console.log({
    continueAccessToken: opPendingGrant.continue.access_token.value,
    continueUri: opPendingGrant.continue.uri,
    interactRef: opPendingGrant.interact.interact_ref,
    quoteId: quote.id,
    senderWalletAddress: senderDetails.id,
  });

  // Return required info to continue payment after user authorization
  return {
    redirectUri: opPendingGrant.interact.redirect,
    continue: {
      continueAccessToken: opPendingGrant.continue.access_token.value,
      continueUri: opPendingGrant.continue.uri,
      interactRef: opPendingGrant.interact.interact_ref,
      quoteId: quote.id,
      senderWalletAddress: senderDetails.id,
    },
  };
}

export async function continueOutgoingPaymentAfterAuth(
  client: AuthenticatedClient,
  continuation: {
    continueAccessToken: string;
    continueUri: string;
    interactRef: string;
    quoteId: string;
    senderWalletAddress: string;
  },
  senderDetails: WalletAddress // You can fetch this again if not stored
) {
  const grant = await client.grant.continue(
    {
      accessToken: continuation.continueAccessToken,
      url: continuation.continueUri,
    },
    {
      interact_ref: continuation.interactRef,
    }
  ) as Grant;

  const outgoingPayment = await client.outgoingPayment.create(
    {
      url: senderDetails.resourceServer,
      accessToken: grant.access_token.value,
    },
    {
      walletAddress: continuation.senderWalletAddress,
      quoteId: continuation.quoteId,
    }
  );

  console.log("Outgoing Payment Created:", outgoingPayment.id);
  return outgoingPayment;
}
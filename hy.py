import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import threading
import time
import random

class FreelanceMarketplace:
    def __init__(self, root):
        self.root = root
        self.root.title("FreelanceHub - Marketplace & Payment System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#fff0f5')  # Light pink background
        
        # User data
        self.user_balance = 5000.00
        self.escrow_balance = 0.00
        self.user_type = tk.StringVar(value='client')
        self.current_user = "Donald Duckson"
        self.wallet_address = "$ilp.interledger-test.dev/testpzar"  # Sample wallet address
        self.messages = {}  # Dictionary to store messages
        
        # Sample freelancers
        self.freelancers = [
            {
                'id': 1,
                'name': 'Sarah Chen',
                'title': 'Full-Stack Developer',
                'rating': 4.9,
                'reviews': 127,
                'hourly_rate': 85,
                'skills': ['Python', 'React', 'Node.js', 'MongoDB'],
                'avatar': '👩‍💻',
                'online': True,
                'portfolio': 'Expert in modern web development with 5+ years experience'
            },
            {
                'id': 2,
                'name': 'Alex Rodriguez',
                'title': 'UI/UX Designer',
                'rating': 4.8,
                'reviews': 89,
                'hourly_rate': 65,
                'skills': ['Figma', 'Adobe XD', 'Sketch', 'Prototyping'],
                'avatar': '🎨',
                'online': True,
                'portfolio': 'Creating beautiful, user-centered designs for web and mobile'
            },
            {
                'id': 3,
                'name': 'Mohammed Hassan',
                'title': 'Mobile App Developer',
                'rating': 4.7,
                'reviews': 156,
                'hourly_rate': 70,
                'skills': ['Flutter', 'React Native', 'iOS', 'Android'],
                'avatar': '📱',
                'online': False,
                'portfolio': 'Building cross-platform mobile applications with modern frameworks'
            },
            {
                'id': 4,
                'name': 'Emma Thompson',
                'title': 'Digital Marketing Expert',
                'rating': 4.9,
                'reviews': 203,
                'hourly_rate': 55,
                'skills': ['SEO', 'PPC', 'Social Media', 'Analytics'],
                'avatar': '📊',
                'online': True,
                'portfolio': 'Driving growth through data-driven marketing strategies'
            },
            {
                'id': 5,
                'name': 'David Kim',
                'title': 'Data Scientist',
                'rating': 4.6,
                'reviews': 74,
                'hourly_rate': 95,
                'skills': ['Python', 'Machine Learning', 'SQL', 'Tableau'],
                'avatar': '🔬',
                'online': True,
                'portfolio': 'Turning data into actionable insights with advanced analytics'
            }
        ]
        
        # Active projects
        self.projects = [
            {
                'id': 1,
                'title': 'E-commerce Platform Development',
                'type': 'project',
                'budget': 2500,
                'status': 'in-progress',
                'freelancer': 'Sarah Chen',
                'client': 'John Doe',
                'deposited': 2500,
                'deadline': '2025-07-15',
                'submitted': True,
                'approval_hours_left': 68,
                'description': 'Build a complete e-commerce platform with payment integration'
            }
        ]
        
        # Notifications
        self.notifications = [
            {'type': 'project', 'message': 'Sarah Chen submitted work for review', 'time': '2 hours ago'},
            {'type': 'payment', 'message': 'Payment of $2,500 deposited to escrow', 'time': '3 days ago'},
            {'type': 'message', 'message': 'New message from Alex Rodriguez', 'time': '1 day ago'}
        ]
        
        self.setup_styles()
        self.setup_gui()
        self.start_timer_thread()
        self.update_balances()
    
    def setup_styles(self):
        # Configure custom styles with pink theme
        style = ttk.Style()
        style.theme_use('clam')
        
        # Background colors
        style.configure('.', background='#fff0f5')  # Light pink
        style.configure('TFrame', background='#fff0f5')
        style.configure('TLabel', background='#fff0f5')
        style.configure('TNotebook', background='#fff0f5')
        style.configure('TNotebook.Tab', background='#ffcce6', padding=[10, 5])  # Light pink tab
        style.map('TNotebook.Tab', background=[('selected', '#ff66b3')])  # Darker pink when selected
        
        # Custom colors
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'), background='#fff0f5', foreground='#ff1493')  # Deep pink
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'), foreground='#ff1493')
        style.configure('Success.TLabel', foreground='#ff66b3')  # Medium pink
        style.configure('Warning.TLabel', foreground='#ff3399')  # Pink
        style.configure('Danger.TLabel', foreground='#cc0066')  # Dark pink
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'), background='#ff66b3', foreground='white')
        
        # LabelFrame style - THIS IS THE FIX FOR THE ERROR
        style.configure('TLabelframe', background='#fff0f5', bordercolor='#ff66b3', lightcolor='#ff66b3', darkcolor='#ff66b3')
        style.configure('TLabelframe.Label', background='#fff0f5', foreground='#ff1493')
        
        # Button styles
        style.map('Primary.TButton',
                 background=[('active', '#ff3399'), ('pressed', '#cc0066')],
                 foreground=[('active', 'white'), ('pressed', 'white')])
    
    def setup_gui(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header
        self.create_header(main_frame)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        # Create tabs
        self.create_marketplace_tab()
        self.create_dashboard_tab()
        self.create_projects_tab()
        self.create_payments_tab()
        self.create_wallet_tab()
        self.create_messages_tab()  # New messages tab
        
        # Start with marketplace tab
        self.notebook.select(0)
    
    def create_header(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Left side - Logo and title
        left_frame = ttk.Frame(header_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        logo_label = ttk.Label(left_frame, text="🚀 FreelanceHub", 
                              font=('Arial', 20, 'bold'), foreground='#ff1493')
        logo_label.pack(side=tk.LEFT)
        
        # Right side - User info and balance
        right_frame = ttk.Frame(header_frame)
        right_frame.pack(side=tk.RIGHT)
        
        # User type selection
        user_frame = ttk.Frame(right_frame)
        user_frame.pack(side=tk.RIGHT, padx=(0, 20))
        
        ttk.Label(user_frame, text="Mode:", font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 5))
        user_combo = ttk.Combobox(user_frame, textvariable=self.user_type, 
                                 values=['client', 'freelancer'], state='readonly', width=10)
        user_combo.pack(side=tk.LEFT)
        user_combo.bind('<<ComboboxSelected>>', self.on_user_type_change)
        
        # Balance display
        balance_frame = ttk.Frame(right_frame)
        balance_frame.pack(side=tk.RIGHT, padx=(0, 20))
        
        ttk.Label(balance_frame, text="💰", font=('Arial', 16)).pack(side=tk.LEFT)
        self.balance_label = ttk.Label(balance_frame, text=f"${self.user_balance:,.2f}", 
                                      font=('Arial', 14, 'bold'), foreground='#ff66b3')
        self.balance_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # User info
        user_info_frame = ttk.Frame(right_frame)
        user_info_frame.pack(side=tk.RIGHT)
        
        ttk.Label(user_info_frame, text="👤", font=('Arial', 16)).pack(side=tk.LEFT)
        ttk.Label(user_info_frame, text=self.current_user, 
                 font=('Arial', 12, 'bold'), foreground='#ff1493').pack(side=tk.LEFT, padx=(5, 0))
    
    def create_marketplace_tab(self):
        marketplace_frame = ttk.Frame(self.notebook)
        self.notebook.add(marketplace_frame, text="🏪 Marketplace")
        
        # Search and filters
        search_frame = ttk.LabelFrame(marketplace_frame, text="Find Freelancers", padding=15)
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        search_row1 = ttk.Frame(search_frame)
        search_row1.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_row1, text="Search:").pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry = ttk.Entry(search_row1, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(search_row1, text="Category:").pack(side=tk.LEFT, padx=(20, 10))
        category_combo = ttk.Combobox(search_row1, values=['All', 'Web Development', 'Mobile Apps', 'Design', 'Marketing', 'Data Science'], 
                                     state='readonly', width=15)
        category_combo.set('All')
        category_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(search_row1, text="🔍 Search", style='Primary.TButton', 
                  command=self.search_freelancers).pack(side=tk.LEFT, padx=(20, 0))
        
        # Freelancers grid
        freelancers_frame = ttk.LabelFrame(marketplace_frame, text="Available Freelancers", padding=15)
        freelancers_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable canvas
        canvas = tk.Canvas(freelancers_frame, bg='#fff0f5', highlightthickness=0)
        scrollbar = ttk.Scrollbar(freelancers_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create freelancer cards
        self.create_freelancer_cards(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_freelancer_cards(self, parent):
        row = 0
        col = 0
        max_cols = 2
        
        for freelancer in self.freelancers:
            # Card frame with pink styling
            card_frame = ttk.LabelFrame(parent, padding=15)
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            
            # Header with avatar and basic info
            header_frame = ttk.Frame(card_frame)
            header_frame.pack(fill=tk.X, pady=(0, 10))
            
            # Avatar and name
            avatar_frame = ttk.Frame(header_frame)
            avatar_frame.pack(side=tk.LEFT, fill=tk.Y)
            
            avatar_label = ttk.Label(avatar_frame, text=freelancer['avatar'], font=('Arial', 24))
            avatar_label.pack()
            
            online_status = "🟢 Online" if freelancer['online'] else "🔴 Offline"
            status_color = '#ff66b3' if freelancer['online'] else '#cc0066'
            status_label = ttk.Label(avatar_frame, text=online_status, font=('Arial', 8), foreground=status_color)
            status_label.pack()
            
            # Info
            info_frame = ttk.Frame(header_frame)
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(15, 0))
            
            name_label = ttk.Label(info_frame, text=freelancer['name'], 
                                  font=('Arial', 14, 'bold'), foreground='#ff1493')
            name_label.pack(anchor=tk.W)
            
            title_label = ttk.Label(info_frame, text=freelancer['title'], 
                                   font=('Arial', 11), foreground='#ff66b3')
            title_label.pack(anchor=tk.W)
            
            # Rating and reviews
            rating_frame = ttk.Frame(info_frame)
            rating_frame.pack(anchor=tk.W, pady=(5, 0))
            
            stars = "⭐" * int(freelancer['rating'])
            rating_label = ttk.Label(rating_frame, text=f"{stars} {freelancer['rating']}", foreground='#ff3399')
            rating_label.pack(side=tk.LEFT)
            
            reviews_label = ttk.Label(rating_frame, text=f"({freelancer['reviews']} reviews)", 
                                     foreground='#ff66b3')
            reviews_label.pack(side=tk.LEFT, padx=(5, 0))
            
            # Rate
            rate_label = ttk.Label(info_frame, text=f"${freelancer['hourly_rate']}/hour", 
                                  font=('Arial', 12, 'bold'), foreground='#ff1493')
            rate_label.pack(anchor=tk.W, pady=(5, 0))
            
            # Skills
            skills_frame = ttk.Frame(card_frame)
            skills_frame.pack(fill=tk.X, pady=(0, 10))
            
            ttk.Label(skills_frame, text="Skills:", font=('Arial', 10, 'bold'), foreground='#ff1493').pack(anchor=tk.W)
            skills_text = " • ".join(freelancer['skills'])
            ttk.Label(skills_frame, text=skills_text, foreground='#ff3399').pack(anchor=tk.W)
            
            # Portfolio
            portfolio_frame = ttk.Frame(card_frame)
            portfolio_frame.pack(fill=tk.X, pady=(0, 10))
            
            portfolio_label = ttk.Label(portfolio_frame, text=freelancer['portfolio'], 
                                       wraplength=400, justify=tk.LEFT, foreground='#cc0066')
            portfolio_label.pack(anchor=tk.W)
            
            # Action buttons
            buttons_frame = ttk.Frame(card_frame)
            buttons_frame.pack(fill=tk.X)
            
            ttk.Button(buttons_frame, text="💬 Message", 
                      command=lambda f=freelancer: self.message_freelancer(f)).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(buttons_frame, text="🚀 Hire Now", 
                      command=lambda f=freelancer: self.hire_freelancer(f)).pack(side=tk.LEFT)
            
            # Grid positioning
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
                
    def create_dashboard_tab(self):
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Stats cards
        stats_frame = ttk.Frame(dashboard_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Active projects card
        active_card = ttk.LabelFrame(stats_frame, text="Active Projects", padding=15)
        active_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(active_card, text="🎯", font=('Arial', 24)).pack()
        self.active_projects_label = ttk.Label(active_card, text=str(len(self.projects)), 
                                              font=('Arial', 28, 'bold'), foreground='#ff1493')
        self.active_projects_label.pack()
        
        # Escrow balance card
        escrow_card = ttk.LabelFrame(stats_frame, text="Funds in Escrow", padding=15)
        escrow_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(escrow_card, text="🔒", font=('Arial', 24)).pack()
        self.escrow_label = ttk.Label(escrow_card, text=f"${self.escrow_balance:,.2f}", 
                                     font=('Arial', 20, 'bold'), foreground='#ff66b3')
        self.escrow_label.pack()
        
        # Pending actions card
        pending_card = ttk.LabelFrame(stats_frame, text="Pending Actions", padding=15)
        pending_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(pending_card, text="⏰", font=('Arial', 24)).pack()
        pending_count = sum(1 for p in self.projects if p.get('submitted', False))
        self.pending_label = ttk.Label(pending_card, text=str(pending_count), 
                                      font=('Arial', 28, 'bold'), foreground='#ff3399')
        self.pending_label.pack()
        
        # Recent activity
        activity_frame = ttk.LabelFrame(dashboard_frame, text="Recent Activity", padding=15)
        activity_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Activity list
        for notification in self.notifications:
            activity_row = ttk.Frame(activity_frame)
            activity_row.pack(fill=tk.X, pady=5)
            
            # Icon based on type
            icons = {'project': '📋', 'payment': '💰', 'message': '💬'}
            icon = icons.get(notification['type'], '📋')
            
            ttk.Label(activity_row, text=icon, font=('Arial', 16), foreground='#ff1493').pack(side=tk.LEFT, padx=(0, 10))
            ttk.Label(activity_row, text=notification['message'], foreground='#cc0066').pack(side=tk.LEFT, fill=tk.X, expand=True)
            ttk.Label(activity_row, text=notification['time'], 
                     foreground='#ff66b3').pack(side=tk.RIGHT)
        
        # Action buttons
        actions_frame = ttk.Frame(dashboard_frame)
        actions_frame.pack(fill=tk.X)
        
        ttk.Button(actions_frame, text="💰 Add Funds", style='Primary.TButton',
                  command=self.add_funds).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actions_frame, text="🔄 Refresh", style='Primary.TButton',
                  command=self.refresh_dashboard).pack(side=tk.LEFT)
    
    def create_projects_tab(self):
        projects_frame = ttk.Frame(self.notebook)
        self.notebook.add(projects_frame, text="📋 My Projects")
        
        # Projects list
        if self.projects:
            for project in self.projects:
                self.create_project_card(projects_frame, project)
        else:
            # Empty state
            empty_frame = ttk.Frame(projects_frame)
            empty_frame.pack(expand=True, fill=tk.BOTH)
            
            ttk.Label(empty_frame, text="📋", font=('Arial', 48), foreground='#ff66b3').pack(pady=20)
            ttk.Label(empty_frame, text="No active projects", 
                     font=('Arial', 16), foreground='#ff1493').pack()
            ttk.Label(empty_frame, text="Visit the marketplace to hire freelancers!", 
                     foreground='#ff66b3').pack(pady=10)
    
    def create_project_card(self, parent, project):
        card_frame = ttk.LabelFrame(parent, padding=20)
        card_frame.pack(fill=tk.X, pady=10)
        
        # Header
        header_frame = ttk.Frame(card_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(header_frame, text=project['title'], 
                 font=('Arial', 16, 'bold'), foreground='#ff1493').pack(side=tk.LEFT)
        
        # Status badge
        status_colors = {
            'in-progress': '#ff66b3',
            'completed': '#ff1493',
            'pending': '#ff3399'
        }
        status_color = status_colors.get(project['status'], '#cc0066')
        status_label = ttk.Label(header_frame, text=project['status'].title(), 
                               foreground=status_color, font=('Arial', 10, 'bold'))
        status_label.pack(side=tk.RIGHT)
        
        # Details
        details_frame = ttk.Frame(card_frame)
        details_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Left column
        left_col = ttk.Frame(details_frame)
        left_col.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(left_col, text=f"💼 Freelancer: {project['freelancer']}", foreground='#cc0066').pack(anchor=tk.W, pady=2)
        ttk.Label(left_col, text=f"💰 Budget: ${project['budget']:,}", foreground='#cc0066').pack(anchor=tk.W, pady=2)
        ttk.Label(left_col, text=f"📅 Deadline: {project['deadline']}", foreground='#cc0066').pack(anchor=tk.W, pady=2)
        
        # Right column
        right_col = ttk.Frame(details_frame)
        right_col.pack(side=tk.RIGHT)
        
        if project.get('submitted'):
            hours_left = project.get('approval_hours_left', 0)
            ttk.Label(right_col, text=f"⏰ Approval needed in {hours_left}h", 
                     foreground='#ff1493', font=('Arial', 10, 'bold')).pack()
            
            # Action buttons
            buttons_frame = ttk.Frame(card_frame)
            buttons_frame.pack(fill=tk.X)
            
            ttk.Button(buttons_frame, text="✅ Approve Work", style='Primary.TButton',
                      command=lambda p=project: self.approve_work(p)).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(buttons_frame, text="🔄 Request Revision", style='Primary.TButton',
                      command=lambda p=project: self.request_revision(p)).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(buttons_frame, text="💬 Message", style='Primary.TButton',
                      command=lambda p=project: self.message_about_project(p)).pack(side=tk.LEFT)
    
    def create_payments_tab(self):
        payments_frame = ttk.Frame(self.notebook)
        self.notebook.add(payments_frame, text="💳 Payments")
        
        # Payment history
        history_frame = ttk.LabelFrame(payments_frame, text="Payment History", padding=15)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Create treeview for payment history with pink styling
        style = ttk.Style()
        style.configure("Treeview", background="#fff0f5", fieldbackground="#fff0f5", foreground="#cc0066")
        style.configure("Treeview.Heading", background="#ff66b3", foreground="white", font=('Arial', 10, 'bold'))
        style.map("Treeview", background=[('selected', '#ff3399')], foreground=[('selected', 'white')])
        
        columns = ('date', 'description', 'amount', 'status')
        history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=10)
        
        history_tree.heading('date', text='Date')
        history_tree.heading('description', text='Description')
        history_tree.heading('amount', text='Amount')
        history_tree.heading('status', text='Status')
        
        history_tree.column('date', width=120)
        history_tree.column('description', width=400)
        history_tree.column('amount', width=120)
        history_tree.column('status', width=100)
        
        # Sample payment data
        payments = [
            ('2025-06-25', 'Escrow deposit for E-commerce Platform Development', '-$2,500.00', 'Completed'),
            ('2025-06-20', 'Wallet top-up via Credit Card', '+$3,000.00', 'Completed'),
            ('2025-06-15', 'Payment to Alex Rodriguez - Logo Design', '-$450.00', 'Completed'),
            ('2025-06-10', 'Refund for cancelled project', '+$800.00', 'Completed'),
        ]
        
        for payment in payments:
            history_tree.insert('', tk.END, values=payment)
        
        history_tree.pack(fill=tk.BOTH, expand=True)
        
        # Payment actions
        actions_frame = ttk.Frame(payments_frame)
        actions_frame.pack(fill=tk.X)
        
        ttk.Button(actions_frame, text="💳 Add Payment Method", style='Primary.TButton',
                  command=self.add_payment_method).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actions_frame, text="📊 Export History", style='Primary.TButton',
                  command=self.export_history).pack(side=tk.LEFT)
    
    def create_wallet_tab(self):
        wallet_frame = ttk.Frame(self.notebook)
        self.notebook.add(wallet_frame, text="💰 Wallet")
        
        # Balance overview
        balance_frame = ttk.LabelFrame(wallet_frame, text="Wallet Overview", padding=20)
        balance_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Available balance
        available_frame = ttk.Frame(balance_frame)
        available_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(available_frame, text="💰 Available Balance:", 
                 font=('Arial', 14), foreground='#ff1493').pack(side=tk.LEFT)
        self.wallet_balance_label = ttk.Label(available_frame, text=f"${self.user_balance:,.2f}", 
                                             font=('Arial', 18, 'bold'), foreground='#ff66b3')
        self.wallet_balance_label.pack(side=tk.RIGHT)
        
        # Escrow balance
        escrow_frame = ttk.Frame(balance_frame)
        escrow_frame.pack(fill=tk.X)
        
        ttk.Label(escrow_frame, text="🔒 Funds in Escrow:", 
                 font=('Arial', 14), foreground='#ff1493').pack(side=tk.LEFT)
        self.wallet_escrow_label = ttk.Label(escrow_frame, text=f"${self.escrow_balance:,.2f}", 
                                            font=('Arial', 18, 'bold'), foreground='#ff3399')
        self.wallet_escrow_label.pack(side=tk.RIGHT)
        
        # Quick actions
        actions_frame = ttk.LabelFrame(wallet_frame, text="Quick Actions", padding=20)
        actions_frame.pack(fill=tk.X, pady=(0, 15))
        
        actions_row = ttk.Frame(actions_frame)
        actions_row.pack(fill=tk.X)
        
        ttk.Button(actions_row, text="💳 Add Funds", style='Primary.TButton',
                  command=self.add_funds).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Button(actions_row, text="🏦 Withdraw", style='Primary.TButton',
                  command=self.withdraw_funds).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Button(actions_row, text="🔄 Auto-Topup", style='Primary.TButton',
                  command=self.setup_auto_topup).pack(side=tk.LEFT)
        
        # Transaction summary
        summary_frame = ttk.LabelFrame(wallet_frame, text="This Month's Summary", padding=15)
        summary_frame.pack(fill=tk.BOTH, expand=True)
        
        summary_data = [
            ("Total Spent", "$3,200.00", "#cc0066"),
            ("Total Earned", "$0.00", "#ff1493"),
            ("Fees Paid", "$96.00", "#ff66b3"),
            ("Refunds Received", "$800.00", "#ff3399")
        ]
        
        for label, amount, color in summary_data:
            row = ttk.Frame(summary_frame)
            row.pack(fill=tk.X, pady=5)
            
            ttk.Label(row, text=label, foreground='#cc0066').pack(side=tk.LEFT)
            ttk.Label(row, text=amount, foreground=color, 
                     font=('Arial', 10, 'bold')).pack(side=tk.RIGHT)
    
    def create_messages_tab(self):
        messages_frame = ttk.Frame(self.notebook)
        self.notebook.add(messages_frame, text="💬 Messages")
        
        # Main message container
        main_msg_frame = ttk.Frame(messages_frame)
        main_msg_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - conversation list
        conv_frame = ttk.LabelFrame(main_msg_frame, text="Conversations", width=200, padding=10)
        conv_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Sample conversations
        conversations = [
            {'name': 'Sarah Chen', 'last_msg': 'I sent the latest update', 'time': '2h ago', 'unread': False},
            {'name': 'Alex Rodriguez', 'last_msg': 'What do you think of the design?', 'time': '1d ago', 'unread': True},
            {'name': 'Emma Thompson', 'last_msg': 'Let me know about the budget', 'time': '3d ago', 'unread': False}
        ]
        
        for conv in conversations:
            conv_btn = ttk.Frame(conv_frame)
            conv_btn.pack(fill=tk.X, pady=2)
            
            # Highlight unread messages
            if conv['unread']:
                conv_btn.configure(style='Unread.TFrame')
                ttk.Style().configure('Unread.TFrame', background='#ffcce6')
            
            ttk.Label(conv_btn, text=conv['name'], font=('Arial', 10, 'bold'), 
                     foreground='#ff1493').pack(anchor=tk.W)
            ttk.Label(conv_btn, text=conv['last_msg'], foreground='#cc0066').pack(anchor=tk.W)
            ttk.Label(conv_btn, text=conv['time'], foreground='#ff66b3', 
                     font=('Arial', 8)).pack(anchor=tk.E)
            
            # Bind click event to load conversation
            conv_btn.bind('<Button-1>', lambda e, c=conv: self.load_conversation(c))
            for child in conv_btn.winfo_children():
                child.bind('<Button-1>', lambda e, c=conv: self.load_conversation(c))
        
        # Right panel - message display and input
        msg_display_frame = ttk.Frame(main_msg_frame)
        msg_display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Current conversation header
        self.msg_header = ttk.Label(msg_display_frame, text="Select a conversation", 
                                   font=('Arial', 12, 'bold'), foreground='#ff1493')
        self.msg_header.pack(anchor=tk.W, pady=(0, 10))
        
        # Message display area
        msg_area_frame = ttk.LabelFrame(msg_display_frame, text="Messages", padding=10)
        msg_area_frame.pack(fill=tk.BOTH, expand=True)
        
        self.msg_text = tk.Text(msg_area_frame, wrap=tk.WORD, state=tk.DISABLED, 
                               bg='white', fg='#cc0066', font=('Arial', 10))
        scrollbar = ttk.Scrollbar(msg_area_frame, command=self.msg_text.yview)
        self.msg_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_text.pack(fill=tk.BOTH, expand=True)
        
        # Message input area
        input_frame = ttk.Frame(msg_display_frame)
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.msg_entry = tk.Text(input_frame, height=3, wrap=tk.WORD, 
                                bg='white', fg='#cc0066', font=('Arial', 10))
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        send_btn = ttk.Button(input_frame, text="Send", style='Primary.TButton',
                            command=self.send_message)
        send_btn.pack(side=tk.RIGHT)
    
    def load_conversation(self, conversation):
        """Load a conversation into the message display"""
        self.msg_header.config(text=f"Conversation with {conversation['name']}")
        self.msg_text.config(state=tk.NORMAL)
        self.msg_text.delete(1.0, tk.END)
        
        # Sample messages (in a real app, these would come from your data store)
        messages = [
            {'sender': conversation['name'], 'text': 'Hello! How are you?', 'time': '10:30 AM'},
            {'sender': self.current_user, 'text': "I'm good, thanks! How about you?", 'time': '10:32 AM'},
            {'sender': conversation['name'], 'text': conversation['last_msg'], 'time': conversation['time']}
        ]
        
        for msg in messages:
            if msg['sender'] == self.current_user:
                # Right-align our messages
                self.msg_text.tag_configure('right', justify='right', foreground='#ff1493')
                self.msg_text.insert(tk.END, f"{msg['text']}\n", 'right')
            else:
                # Left-align other messages
                self.msg_text.tag_configure('left', justify='left', foreground='#cc0066')
                self.msg_text.insert(tk.END, f"{msg['sender']}: {msg['text']}\n", 'left')
            
            # Add timestamp
            self.msg_text.tag_configure('time', foreground='#ff66b3', font=('Arial', 8))
            self.msg_text.insert(tk.END, f"{msg['time']}\n\n", 'time')
        
        self.msg_text.config(state=tk.DISABLED)
        self.current_conversation = conversation['name']
    
    def send_message(self):
        message = self.msg_entry.get("1.0", tk.END).strip()
        if message and hasattr(self, 'current_conversation'):
            # In a real app, you would save this message to your data store
            self.msg_text.config(state=tk.NORMAL)
            self.msg_text.tag_configure('right', justify='right', foreground='#ff1493')
            self.msg_text.insert(tk.END, f"{message}\n", 'right')
            
            # Add timestamp
            now = datetime.now().strftime("%I:%M %p")
            self.msg_text.tag_configure('time', foreground='#ff66b3', font=('Arial', 8))
            self.msg_text.insert(tk.END, f"{now}\n\n", 'time')
            
            self.msg_text.config(state=tk.DISABLED)
            self.msg_entry.delete("1.0", tk.END)
            
            # Auto-scroll to bottom
            self.msg_text.see(tk.END)
    
    def hire_freelancer(self, freelancer):
        # Create hire dialog with larger size
        hire_window = tk.Toplevel(self.root)
        hire_window.title(f"Hire {freelancer['name']}")
        hire_window.geometry("600x500")  # Larger window size
        hire_window.grab_set()
        
        # Freelancer info
        info_frame = ttk.LabelFrame(hire_window, text="Freelancer Details", padding=15)
        info_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(info_frame, text=f"{freelancer['avatar']} {freelancer['name']}", 
                 font=('Arial', 16, 'bold'), foreground='#ff1493').pack(anchor=tk.W)
        ttk.Label(info_frame, text=freelancer['title'], 
                 foreground='#ff66b3').pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Rate: ${freelancer['hourly_rate']}/hour", 
                 font=('Arial', 12, 'bold'), foreground='#ff1493').pack(anchor=tk.W, pady=(5, 0))
        
        # Project details
        project_frame = ttk.LabelFrame(hire_window, text="Project Details", padding=15)
        project_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        ttk.Label(project_frame, text="Project Title:", foreground='#cc0066').pack(anchor=tk.W)
        title_entry = ttk.Entry(project_frame)
        title_entry.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(project_frame, text="Project Description:", foreground='#cc0066').pack(anchor=tk.W)
        desc_text = tk.Text(project_frame, height=5)
        desc_text.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(project_frame, text="Project Type:", foreground='#cc0066').pack(anchor=tk.W)
        type_combo = ttk.Combobox(project_frame, values=["Hourly", "Fixed Price"], state="readonly")
        type_combo.set("Fixed Price")
        type_combo.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(project_frame, text="Budget:", foreground='#cc0066').pack(anchor=tk.W)
        budget_entry = ttk.Entry(project_frame)
        budget_entry.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(project_frame, text="Deadline:", foreground='#cc0066').pack(anchor=tk.W)
        deadline_entry = ttk.Entry(project_frame)
        deadline_entry.pack(fill=tk.X, pady=(0, 10))
        deadline_entry.insert(0, (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"))
        
        
        
         # Payment method
        payment_frame = ttk.LabelFrame(hire_window, text="Payment Method", padding=15)
        payment_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        payment_var = tk.StringVar(value="wallet")
        ttk.Radiobutton(payment_frame, text="Use Wallet Balance", variable=payment_var, value="wallet").pack(anchor=tk.W)
        ttk.Radiobutton(payment_frame, text="Credit Card (**** 1234)", variable=payment_var, value="card").pack(anchor=tk.W)
        
        # Action buttons
        button_frame = ttk.Frame(hire_window)
        button_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        def create_project():
            title = title_entry.get()
            description = desc_text.get("1.0", tk.END).strip()
            budget = float(budget_entry.get())
            deadline = deadline_entry.get()
            
            new_project = {
                'id': len(self.projects) + 1,
                'title': title,
                'type': 'project',
                'budget': budget,
                'status': 'in-progress',
                'freelancer': freelancer['name'],
                'client': self.current_user,
                'deposited': budget,
                'deadline': deadline,
                'submitted': False,
                'description': description
            }
            
            # Deduct from balance and add to escrow
            if payment_var.get() == "wallet":
                if budget > self.user_balance:
                    messagebox.showerror("Error", "Insufficient funds in wallet")
                    return
                self.user_balance -= budget
                self.escrow_balance += budget
                self.update_balances()
            
            self.projects.append(new_project)
            
            # Update UI
            self.refresh_projects_tab()
            self.notebook.select(2)  # Switch to projects tab
            
            messagebox.showinfo("Success", f"You've hired {freelancer['name']} for your project!")
            hire_window.destroy()
        
        ttk.Button(button_frame, text="Cancel", command=hire_window.destroy).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Hire Freelancer", style="Primary.TButton", 
                  command=create_project).pack(side=tk.RIGHT)
    
    def refresh_projects_tab(self):
        # Clear the current projects tab
        for widget in self.notebook.winfo_children()[2].winfo_children():
            widget.destroy()
        
        # Recreate the projects tab content
        self.create_projects_tab()
    
    def update_balances(self):
        self.balance_label.config(text=f"${self.user_balance:,.2f}")
        self.escrow_label.config(text=f"${self.escrow_balance:,.2f}")
        self.wallet_balance_label.config(text=f"${self.user_balance:,.2f}")
        self.wallet_escrow_label.config(text=f"${self.escrow_balance:,.2f}")
    
    def search_freelancers(self):
        search_term = self.search_entry.get().lower()
        if search_term:
            messagebox.showinfo("Search", f"Searching for: {search_term}")
        else:
            messagebox.showinfo("Search", "Showing all freelancers")
    
    def message_freelancer(self, freelancer):
        # Open the messages tab and load the conversation
        self.notebook.select(5)  # Switch to messages tab
        
        # Create a fake conversation if it doesn't exist
        if freelancer['name'] not in self.messages:
            self.messages[freelancer['name']] = [
                {'sender': freelancer['name'], 'text': f"Hello! I'm {freelancer['name']}, ready to work with you!", 'time': 'Just now'}
            ]
        
        # Load the conversation
        self.load_conversation({
            'name': freelancer['name'],
            'last_msg': self.messages[freelancer['name']][-1]['text'],
            'time': self.messages[freelancer['name']][-1]['time'],
            'unread': False
        })
    
    def on_user_type_change(self, event):
        new_type = self.user_type.get()
        if new_type == 'freelancer':
            messagebox.showinfo("Mode Changed", "Switched to Freelancer mode - now you can see available projects to bid on")
            # In a real app, you would update the UI to show freelancer-specific content
        else:
            messagebox.showinfo("Mode Changed", "Switched to Client mode - now you can hire freelancers")
            # In a real app, you would update the UI to show client-specific content
    
    def add_funds(self):
        # First ask for wallet address
        wallet = simpledialog.askstring("Wallet Address", "Enter your wallet address:", 
                                      initialvalue=self.wallet_address)
        if not wallet:
            return  # User cancelled
        
        # Then ask for amount
        amount = simpledialog.askfloat("Add Funds", f"Adding funds from wallet {wallet}\nEnter amount to add:")
        if amount and amount > 0:
            self.user_balance += amount
            self.update_balances()
            messagebox.showinfo("Success", f"Added ${amount:,.2f} to your wallet")
    
    def withdraw_funds(self):
        wallet = simpledialog.askstring("Wallet Address", "Enter withdrawal wallet address:", 
                                      initialvalue=self.wallet_address)
        if not wallet:
            return  # User cancelled
            
        amount = simpledialog.askfloat("Withdraw Funds", f"Withdrawing to {wallet}\nEnter amount to withdraw:")
        if amount and amount > 0:
            if amount > self.user_balance:
                messagebox.showerror("Error", "Insufficient funds in wallet")
            else:
                self.user_balance -= amount
                self.update_balances()
                messagebox.showinfo("Success", f"Withdrew ${amount:,.2f} to {wallet}")
    
    def setup_auto_topup(self):
        wallet = simpledialog.askstring("Wallet Address", "Enter your wallet address for auto-topup:", 
                                      initialvalue=self.wallet_address)
        if wallet:
            amount = simpledialog.askfloat("Auto-Topup", "Enter amount to auto-topup when balance is low:")
            if amount and amount > 0:
                messagebox.showinfo("Auto-Topup Set", f"Will auto-topup ${amount} from {wallet} when balance is low")
    
    def add_payment_method(self):
        # Create a larger window for adding payment method
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Add Payment Method")
        payment_window.geometry("500x400")
        
        ttk.Label(payment_window, text="Add New Payment Method", 
                 font=('Arial', 14, 'bold'), foreground='#ff1493').pack(pady=10)
        
        # Payment type selection
        type_frame = ttk.Frame(payment_window)
        type_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(type_frame, text="Payment Type:", foreground='#cc0066').pack(anchor=tk.W)
        payment_type = ttk.Combobox(type_frame, values=["Credit Card", "Bank Account", "Crypto Wallet"], 
                                   state="readonly")
        payment_type.set("Credit Card")
        payment_type.pack(fill=tk.X)
        
        # Card details
        details_frame = ttk.LabelFrame(payment_window, text="Payment Details", padding=15)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(details_frame, text="Card Number:", foreground='#cc0066').pack(anchor=tk.W)
        ttk.Entry(details_frame).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(details_frame, text="Expiration Date:", foreground='#cc0066').pack(anchor=tk.W)
        ttk.Entry(details_frame).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(details_frame, text="CVV:", foreground='#cc0066').pack(anchor=tk.W)
        ttk.Entry(details_frame).pack(fill=tk.X, pady=(0, 10))
        
        # Save button
        ttk.Button(payment_window, text="Save Payment Method", style='Primary.TButton',
                  command=lambda: messagebox.showinfo("Success", "Payment method added") and payment_window.destroy()).pack(pady=10)
    
    def export_history(self):
        # Create a larger export dialog
        export_window = tk.Toplevel(self.root)
        export_window.title("Export Payment History")
        export_window.geometry("500x300")
        
        ttk.Label(export_window, text="Export Payment History", 
                 font=('Arial', 14, 'bold'), foreground='#ff1493').pack(pady=10)
        
        # Format selection
        format_frame = ttk.Frame(export_window)
        format_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(format_frame, text="Export Format:", foreground='#cc0066').pack(anchor=tk.W)
        export_format = ttk.Combobox(format_frame, values=["CSV", "Excel", "PDF"], 
                                    state="readonly")
        export_format.set("CSV")
        export_format.pack(fill=tk.X)
        
        # Date range
        date_frame = ttk.Frame(export_window)
        date_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(date_frame, text="Date Range:", foreground='#cc0066').pack(anchor=tk.W)
        
        range_frame = ttk.Frame(date_frame)
        range_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(range_frame, text="From:").pack(side=tk.LEFT)
        ttk.Entry(range_frame, width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(range_frame, text="To:").pack(side=tk.LEFT, padx=(10, 0))
        ttk.Entry(range_frame, width=10).pack(side=tk.LEFT, padx=5)
        
        # Export button
        ttk.Button(export_window, text="Export", style='Primary.TButton',
                  command=lambda: messagebox.showinfo("Exported", "Payment history exported successfully") and export_window.destroy()).pack(pady=10)
    
    def approve_work(self, project):
        confirm = messagebox.askyesno("Approve Work", 
                                    f"Release ${project['budget']} to {project['freelancer']}?")
        if confirm:
            self.escrow_balance -= project['budget']
            project['status'] = 'completed'
            project['submitted'] = False
            self.refresh_projects_tab()
            self.update_balances()
            messagebox.showinfo("Success", "Payment released to freelancer")
    
    def request_revision(self, project):
        message = simpledialog.askstring("Request Revision", 
                                       f"Send revision request to {project['freelancer']}:")
        if message:
            project['submitted'] = False
            project['approval_hours_left'] = 72  # Reset timer
            self.refresh_projects_tab()
            messagebox.showinfo("Success", "Revision request sent")
    
    def message_about_project(self, project):
        # Open messages tab and load conversation with freelancer
        self.notebook.select(5)  # Switch to messages tab
        
        # Create a fake conversation if it doesn't exist
        if project['freelancer'] not in self.messages:
            self.messages[project['freelancer']] = [
                {'sender': project['freelancer'], 'text': f"Hello! I'm working on your project: {project['title']}", 'time': 'Just now'}
            ]
        
        # Load the conversation
        self.load_conversation({
            'name': project['freelancer'],
            'last_msg': self.messages[project['freelancer']][-1]['text'],
            'time': self.messages[project['freelancer']][-1]['time'],
            'unread': False
        })
    
    def refresh_dashboard(self):
        messagebox.showinfo("Refresh", "Dashboard refreshed")
    
    def start_timer_thread(self):
        def update_project_timers():
            while True:
                time.sleep(3600)  # Update every hour
                for project in self.projects:
                    if project.get('submitted', False) and project.get('approval_hours_left', 0) > 0:
                        project['approval_hours_left'] -= 1
                        if project['approval_hours_left'] <= 0:
                            # Auto-approve if time runs out
                            self.escrow_balance -= project['budget']
                            project['status'] = 'completed'
                            project['submitted'] = False
                
                # Update UI if needed
                self.root.after(0, self.refresh_projects_tab)
                self.root.after(0, self.update_balances)
        
        timer_thread = threading.Thread(target=update_project_timers, daemon=True)
        timer_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = FreelanceMarketplace(root)
    root.mainloop()
# Bank Management System - Complete Project Documentation

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [User Roles & Access Levels](#2-user-roles--access-levels)
3. [Core Functionalities](#3-core-functionalities-role-wise)
4. [Feature Categories](#4-feature-categories)
5. [Detailed Feature Breakdown](#5-detailed-feature-breakdown)
6. [Backend Architecture](#6-backend-architecture)
7. [Frontend Architecture](#7-frontend-architecture)
8. [Database Design](#8-database-design)
9. [Deployment & Environment](#9-deployment--environment)
10. [Security Considerations](#10-security-considerations)
11. [Limitations](#11-limitations-of-the-project)
12. [Future Enhancements](#12-future-enhancements)
13. [Interview Guide](#13-how-to-explain-this-project-in-an-interview)
14. [Summary](#14-summary)

---

## 1. PROJECT OVERVIEW

### What is the Bank Management System?

The **Bank Management System** is a full-stack web application that simulates core banking operations in a digital environment. Built with Django (Python), it provides a comprehensive platform where:

- **Customers** can manage their bank accounts and perform transactions
- **Bank Managers** can oversee operations, monitor accounts, and manage users
- **System Administrators** have complete control over the entire system

**Project Type:** Educational/Portfolio Web Application  
**Level:** Beginner to Intermediate  
**Purpose:** Learning, skill demonstration, real-world workflow simulation

**⚠️ Important Note:** This is a learning project and NOT intended for real banking operations. It does not include banking compliance, regulatory features, or production-grade security measures required for actual financial systems.


### What Problem Does It Solve?

**Real-World Context:**

Traditional banking requires physical presence for many operations. This system demonstrates how modern digital banking platforms work by addressing:

**For Customers:**
- ✅ 24/7 access to account information
- ✅ Instant transaction processing (deposits/withdrawals)
- ✅ Digital transaction history and record keeping
- ✅ No need to visit physical branches for basic operations
- ✅ Real-time balance updates

**For Bank Managers:**
- ✅ Centralized monitoring of all accounts and users
- ✅ Real-time transaction oversight
- ✅ Account control capabilities (freeze/unfreeze)
- ✅ System-wide reporting and analytics
- ✅ Audit trail for all management actions

**For System Administrators:**
- ✅ Complete system control and configuration
- ✅ User and role management
- ✅ Database administration
- ✅ System monitoring and troubleshooting

### Who Are the Users of This System?

**Three Distinct User Types:**

1. **Bank Customers (Regular Users)**
   - Individuals who register for bank accounts
   - Perform personal banking operations
   - View their own account information

2. **Bank Managers (Staff)**
   - Bank employees with management responsibilities
   - Oversee customer accounts and transactions
   - Have elevated privileges for monitoring and control

3. **System Administrators (Superusers)**
   - Technical staff or system owners
   - Highest level of access
   - Manage the entire system infrastructure



---

## 2. USER ROLES & ACCESS LEVELS

### Role 1: Admin (System Administrator)

**Who They Are:**
- Technical staff or system owners
- Created via Django's `createsuperuser` command
- Highest level of system access

**What They Can Do:**
- ✅ Access Django Admin Panel (backend interface at `/admin/`)
- ✅ View and modify all database records
- ✅ Perform bulk operations on accounts and transactions
- ✅ Create, edit, and delete users, managers, and accounts
- ✅ Access special admin dashboard in the main UI
- ✅ View complete system statistics and analytics
- ✅ Monitor all manager actions and audit trails
- ✅ Configure system settings

**Access Level:** **FULL SYSTEM ACCESS**

**Cannot Do:**
- Nothing - admins have unrestricted access

**Use Case Example:**
> "As a system admin, I need to view all transactions in the system, identify suspicious activity, and freeze multiple accounts at once using bulk actions."

---

### Role 2: Manager (Bank Manager)

**Who They Are:**
- Bank employees with management responsibilities
- Have a unique employee ID
- Separate login system from regular customers
- Created via web registration or management command

**What They Can Do:**
- ✅ View all customer accounts and details
- ✅ Monitor all system transactions
- ✅ **Freeze accounts** (prevents all transactions)
- ✅ **Unfreeze accounts** (restores normal operation)
- ✅ Approve or reject pending transactions
- ✅ Search and filter users and accounts
- ✅ Generate system-wide reports and analytics
- ✅ View dashboard with system statistics
- ✅ All actions are automatically logged for audit trails

**Access Level:** **MANAGEMENT & OVERSIGHT**

**Cannot Do:**
- ❌ Access Django admin panel
- ❌ Modify system settings
- ❌ Delete database records directly
- ❌ Perform transactions on behalf of customers
- ❌ View or modify other managers' credentials

**Use Case Example:**
> "As a bank manager, I notice unusual withdrawal activity on an account. I can freeze the account immediately, review the transaction history, and contact the customer for verification."



---

### Role 3: Customer (Normal Bank User)

**Who They Are:**
- Regular users who register for bank accounts
- Automatically receive a unique account number upon registration
- Use the system for personal banking needs

**What They Can Do:**
- ✅ Register and create a new account
- ✅ Login to personal dashboard
- ✅ View account balance and account number
- ✅ **Deposit money** into their account
- ✅ **Withdraw money** (with balance validation)
- ✅ View complete transaction history
- ✅ See account status (Active/Frozen)
- ✅ Receive real-time balance updates

**Access Level:** **PERSONAL ACCOUNT ONLY**

**Cannot Do:**
- ❌ View other users' accounts or transactions
- ❌ Access manager or admin features
- ❌ Perform transactions if account is frozen
- ❌ Modify account number or system data
- ❌ Delete their own account

**Use Case Example:**
> "As a customer, I want to check my account balance, deposit my salary, and view my transaction history to track my spending - all from my phone without visiting a branch."

---

## 3. CORE FUNCTIONALITIES (ROLE-WISE)

### Admin Functionalities

**1. Django Admin Panel Access**
- **URL:** `/admin/`
- Enhanced interface with custom actions and visual indicators
- Color-coded status badges for quick identification
- Bulk operations for efficiency

**2. Database Management**
- View all users, accounts, transactions in organized tables
- Bulk approve/reject transactions
- Bulk freeze/unfreeze accounts
- Advanced filtering and search capabilities
- Export data for analysis

**3. Admin Dashboard (UI)**
- System overview with real-time statistics
- Total users, accounts, and system balance
- Transaction summaries (deposits, withdrawals, pending)
- Manager action logs for accountability
- Quick links to admin panel sections

**4. User Management**
- Create, edit, and delete user accounts
- Assign or remove manager roles
- Reset user passwords
- View user activity and login history



---

### Manager Functionalities

**1. Manager Dashboard**
- System statistics overview (users, accounts, balance, transactions)
- Today's transaction count
- Pending approvals count
- Frozen accounts count
- Total deposits and withdrawals
- Recent transactions list

**2. User Management**
- View all registered users
- Search users by username or email
- View detailed user information
- See user's linked account details
- Monitor user activity

**3. Account Management**
- View all bank accounts
- Search by account number or username
- View account details (balance, status, transaction history)
- **Freeze accounts** - Prevents all transactions
- **Unfreeze accounts** - Restores normal operation
- View account creation date and last activity

**4. Transaction Monitoring**
- View all system transactions
- Filter by type (Deposit/Withdrawal)
- Filter by status (Completed/Pending/Failed)
- Filter by date range
- View transaction details and timestamps

**5. Approval System**
- View pending transactions queue
- Approve transactions (changes status to APPROVED)
- Reject transactions (changes status to REJECTED)
- Add notes/reasons for decisions

**6. Reports & Analytics**
- System-wide statistics
- User growth metrics
- Transaction volume analysis
- Account status distribution
- Financial summaries

**7. Audit Trail**
- All manager actions automatically logged
- View action history (who did what and when)
- Accountability and transparency
- Cannot be modified or deleted by managers

---

### Customer Functionalities

**1. Registration & Authentication**
- Register with username, email, and password
- Automatic account creation upon successful registration
- Unique account number generation (format: ACC + 7 random digits)
- Secure login system with session management

**2. Personal Dashboard**
- View account number
- View current balance (in Indian Rupees ₹)
- View account status (Active/Frozen)
- View last activity timestamp
- Quick access buttons for deposit and withdraw

**3. Deposit Money**
- Enter amount to deposit
- Instant balance update
- Transaction record created automatically
- Success/error messages displayed
- Redirected to dashboard with updated balance

**4. Withdraw Money**
- Enter amount to withdraw
- Balance validation (checks for sufficient funds)
- Instant balance update if successful
- Transaction record created
- Cannot withdraw if account is frozen
- Error messages for invalid operations

**5. Transaction History**
- View all personal transactions
- See transaction type (Deposit/Withdrawal)
- See amount and date/time
- See balance after each transaction
- See transaction status
- Sorted by most recent first

**6. Account Status Monitoring**
- See if account is Active or Frozen
- Warning banner displayed if account is frozen
- Deposit/withdraw buttons disabled when frozen
- Clear messaging about account restrictions



---

## 4. FEATURE CATEGORIES

### Authentication & Authorization

**What It Includes:**
- User registration with validation (unique username, valid email, strong password)
- Secure login with password hashing (PBKDF2 algorithm)
- Logout functionality with session cleanup
- Session management and timeout
- Role-based access control (customer, manager, admin)
- Login required decorators for protected views
- Separate manager authentication system

**Why It's Important:**
- Protects user data and privacy
- Ensures only authorized access to features
- Prevents unauthorized transactions
- Maintains system security and integrity
- Demonstrates understanding of web security

---

### Account Management

**What It Includes:**
- Automatic account creation on user registration
- Unique account number generation (ACC + 7 digits)
- Account status management (Active/Frozen)
- Balance tracking with decimal precision
- Last activity timestamp
- Account freeze/unfreeze by managers
- One account per user (OneToOne relationship)

**Why It's Important:**
- Core banking functionality
- Tracks user financial data accurately
- Enables transaction processing
- Provides account control mechanisms
- Demonstrates database relationships

---

### Transaction Management

**What It Includes:**
- Deposit functionality with amount validation
- Withdrawal functionality with balance checking
- Transaction history with complete details
- Transaction status tracking (Completed, Pending, Failed, Approved, Rejected)
- Balance validation before withdrawals
- Atomic operations (all-or-nothing database transactions)
- Transaction timestamps for audit trails

**Why It's Important:**
- Core banking operations
- Financial record keeping and compliance
- Audit trail for disputes
- User transparency and trust
- Demonstrates ACID properties understanding

---

### Approval System

**What It Includes:**
- Pending transaction queue for managers
- Manager approval workflow
- Approve/reject actions with logging
- Status updates reflected in real-time
- Action logging for accountability

**Why It's Important:**
- Additional security layer
- Fraud prevention mechanism
- Manager oversight capability
- Compliance simulation
- Demonstrates workflow management

---

### Report Management

**What It Includes:**
- System statistics dashboard
- User metrics and growth tracking
- Transaction summaries and trends
- Financial reports (deposits, withdrawals, balance)
- Account status distribution
- Date range filtering

**Why It's Important:**
- Business intelligence and insights
- Data-driven decision making
- Performance monitoring
- Trend analysis
- Demonstrates data aggregation skills

---

### Dashboard & UI

**What It Includes:**
- Responsive design (mobile, tablet, desktop)
- Black & white minimalist theme
- Role-specific dashboards (customer, manager, admin)
- Hamburger menu for mobile navigation
- Clean and intuitive navigation
- Status indicators and badges
- Real-time data display
- Success/error message system

**Why It's Important:**
- User experience and satisfaction
- Accessibility across devices
- Professional appearance
- Easy navigation and usability
- Demonstrates frontend skills

---

### Security & Validation

**What It Includes:**
- Password hashing (PBKDF2 with salt)
- CSRF protection on all forms
- Input validation (amount, email, username)
- Balance validation before withdrawals
- Frozen account checks
- SQL injection prevention (Django ORM)
- XSS protection (Django template escaping)
- Session security

**Why It's Important:**
- Data protection and privacy
- Prevent fraud and unauthorized access
- System integrity and reliability
- User trust and confidence
- Demonstrates security awareness



---

## 5. DETAILED FEATURE BREAKDOWN

### Feature: User Registration

**What It Does:**
- Allows new users to create an account in the system
- Collects username, email, and password
- Validates input (unique username, valid email format, password strength)
- Creates user record in database
- Automatically creates linked bank account via Django signal
- Generates unique account number
- Logs user in automatically after registration
- Redirects to dashboard

**Who Can Access It:**
- Anyone (public access, no login required)
- **URL:** `/users/register/`

**Why It's Important:**
- Entry point for new customers
- Onboarding process demonstration
- User acquisition flow
- Shows form handling and validation
- Demonstrates Django signals usage

**Technical Implementation:**
```python
# Form validation
- Username: unique, 3-150 characters
- Email: valid format, unique
- Password: minimum 8 characters, complexity rules

# Automatic account creation via signal
@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
```

---

### Feature: Deposit Money

**What It Does:**
- Allows customers to add money to their account
- Validates amount (must be positive number)
- Updates account balance atomically
- Creates transaction record with details
- Updates last activity timestamp
- Shows success message
- Redirects to dashboard with updated balance

**Who Can Access It:**
- Logged-in customers only
- **URL:** `/bank/deposit/`
- Protected by `@login_required` decorator

**Why It's Important:**
- Core banking operation
- Increases account balance
- Demonstrates transaction processing
- Shows database updates and atomic operations
- Real-world banking simulation

**Technical Implementation:**
```python
# Atomic transaction
with transaction.atomic():
    account.balance += amount
    account.last_activity = timezone.now()
    account.save()
    
    Transaction.objects.create(
        account=account,
        transaction_type='DEPOSIT',
        amount=amount,
        balance_after=account.balance,
        status='COMPLETED'
    )
```

---

### Feature: Withdraw Money

**What It Does:**
- Allows customers to withdraw money from their account
- Validates amount (positive, sufficient balance)
- Checks if account is frozen (prevents withdrawal if frozen)
- Updates account balance atomically
- Creates transaction record
- Shows success/error message
- Prevents overdrafts

**Who Can Access It:**
- Logged-in customers only
- **URL:** `/bank/withdraw/`
- Protected by `@login_required` decorator

**Why It's Important:**
- Core banking operation
- Demonstrates validation logic
- Shows error handling
- Prevents overdrafts and fraud
- Business rule implementation

**Validation Rules:**
1. Amount must be positive
2. Amount must not exceed current balance
3. Account must not be frozen
4. User must be authenticated

---

### Feature: Account Freeze/Unfreeze

**What It Does:**
- Manager can freeze a customer account
- Frozen accounts cannot perform any transactions
- Manager can unfreeze to restore normal access
- Action is logged in ManagerAction table for audit
- Customer sees warning banner when account is frozen
- Deposit/withdraw buttons are disabled for frozen accounts

**Who Can Access It:**
- Bank managers only
- **URLs:** `/bank/manager/freeze/<account_id>/`, `/bank/manager/unfreeze/<account_id>/`
- Protected by `@manager_required` decorator

**Why It's Important:**
- Risk management and fraud prevention
- Account control mechanism
- Demonstrates authorization logic
- Shows role-based access control
- Real-world banking security feature

**Use Case Scenarios:**
- Suspicious activity detected
- Customer reports unauthorized access
- Account under investigation
- Temporary suspension requested by customer

---

### Feature: Transaction History

**What It Does:**
- Displays all transactions for a user
- Shows date/time, type, amount, balance after
- Shows transaction status
- Sorted by most recent first
- Paginated for large datasets
- Filterable by date range (for managers)

**Who Can Access It:**
- **Customers:** View their own transactions only
- **Managers:** View all system transactions
- **URL:** `/bank/transactions/`

**Why It's Important:**
- Transparency and trust
- Record keeping and compliance
- Dispute resolution
- Audit trail
- Financial tracking

**Data Displayed:**
- Transaction ID
- Date and time
- Transaction type (Deposit/Withdrawal)
- Amount (in ₹)
- Balance after transaction
- Status (Completed/Pending/Failed)

---

### Feature: Manager Dashboard

**What It Does:**
- Shows system-wide statistics in real-time
- Displays total users, accounts, and system balance
- Shows today's transaction count
- Shows pending approvals count
- Shows frozen accounts count
- Displays total deposits and withdrawals
- Shows recent transactions list
- Provides quick navigation to all manager features

**Who Can Access It:**
- Bank managers only
- **URL:** `/bank/manager/dashboard/`
- Protected by `@manager_required` decorator

**Why It's Important:**
- Centralized overview for decision making
- Quick insights into system health
- Performance monitoring
- Operational efficiency
- Demonstrates data aggregation

**Statistics Shown:**
- Total Users
- Total Accounts
- Total System Balance
- Today's Transactions
- Pending Approvals
- Frozen Accounts
- Total Deposits
- Total Withdrawals

---

### Feature: Responsive Mobile Menu

**What It Does:**
- Hamburger menu icon appears on mobile devices
- Clicking opens slide-in sidebar from right
- Dark overlay appears behind sidebar
- Smooth animations for open/close
- Auto-closes when clicking outside or on a link
- Menu items displayed vertically with white text
- Works on all screen sizes below 768px

**Who Can Access It:**
- All authenticated users on mobile devices
- Automatically appears on screens < 768px width

**Why It's Important:**
- Mobile user experience
- Modern UI/UX pattern
- Accessibility on all devices
- Professional appearance
- Demonstrates responsive design skills

**Technical Implementation:**
- CSS media queries for responsive breakpoints
- JavaScript for menu toggle functionality
- CSS transitions for smooth animations
- Event listeners for outside clicks



---

## 6. BACKEND ARCHITECTURE

### Django Project Structure

```
BankManagementSystem/
├── manage.py                      # Django CLI tool
├── db.sqlite3                     # SQLite database
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
│
├── config/                        # Project configuration
│   ├── __init__.py
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Main URL routing
│   ├── wsgi.py                   # WSGI server config
│   ├── asgi.py                   # ASGI server config
│   └── production_settings.py    # Production settings
│
├── apps/                          # Django applications
│   ├── __init__.py
│   ├── users/                    # User authentication app
│   │   ├── __init__.py
│   │   ├── models.py            # User-related models
│   │   ├── views.py             # Auth views (login, register, logout)
│   │   ├── forms.py             # Registration forms
│   │   └── urls.py              # Auth URL patterns
│   │
│   └── bank/                     # Banking operations app
│       ├── __init__.py
│       ├── models.py            # Account, Transaction, Manager models
│       ├── views.py             # Customer views
│       ├── manager_views.py     # Manager-specific views
│       ├── forms.py             # Banking forms
│       ├── manager_forms.py     # Manager forms
│       ├── admin.py             # Django admin customization
│       ├── urls.py              # Banking URL patterns
│       └── management/
│           └── commands/
│               └── create_manager.py  # Custom management command
│
├── templates/                     # HTML templates
│   ├── base.html                 # Base template with navbar
│   ├── home.html                 # Landing page
│   ├── users/                    # Auth templates
│   │   ├── login.html
│   │   └── register.html
│   └── bank/                     # Banking templates
│       ├── dashboard.html
│       ├── admin_dashboard.html
│       ├── deposit.html
│       ├── withdraw.html
│       ├── transactions.html
│       └── manager_*.html        # 14 manager templates
│
└── static/                        # Static files
    ├── css/
    │   └── style.css             # Main stylesheet (27KB)
    └── js/
        └── main.js               # JavaScript (menu toggle, etc.)
```

---

### Apps Used

**1. users app**
- **Purpose:** Handle user authentication and authorization
- **Responsibilities:**
  - User registration
  - Login/logout functionality
  - Home/landing page
  - Session management
- **Models:** Uses Django's built-in User model
- **Views:** register_view, login_view, logout_view, home_view

**2. bank app**
- **Purpose:** Handle all banking operations
- **Responsibilities:**
  - Account management
  - Transactions (deposit/withdraw)
  - Manager operations
  - Admin dashboard
  - Reports and analytics
- **Models:** Account, Transaction, BankManager, ManagerAction
- **Views:** 30+ views for customers, managers, and admins

---

### Models, Views, URLs, Templates Concept

**Django MVT (Model-View-Template) Pattern:**

**1. Models (Database Layer)**
- Define database structure using Python classes
- Each class maps to a database table
- Handle data validation and business logic
- Define relationships between tables

**Example:**
```python
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=[
        ('ACTIVE', 'Active'),
        ('FROZEN', 'Frozen')
    ], default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
```

**2. Views (Business Logic Layer)**
- Handle HTTP requests
- Process data and business logic
- Interact with models (database)
- Return HTTP responses
- Render templates with context data

**Example:**
```python
@login_required
def deposit_view(request):
    account = Account.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            # Atomic transaction
            with transaction.atomic():
                account.balance += amount
                account.save()
                
                Transaction.objects.create(
                    account=account,
                    transaction_type='DEPOSIT',
                    amount=amount,
                    balance_after=account.balance,
                    status='COMPLETED'
                )
            
            messages.success(request, f'₹{amount} deposited successfully!')
            return redirect('bank:dashboard')
    else:
        form = DepositForm()
    
    return render(request, 'bank/deposit.html', {'form': form})
```

**3. URLs (Routing Layer)**
- Map URLs to views
- Define URL patterns with parameters
- Handle URL namespacing
- Support RESTful routing

**Example:**
```python
# apps/bank/urls.py
app_name = 'bank'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('transactions/', views.transactions_view, name='transactions'),
    
    # Manager URLs
    path('manager/dashboard/', manager_views.manager_dashboard_view, name='manager_dashboard'),
    path('manager/users/', manager_views.manager_users_view, name='manager_users'),
    path('manager/freeze/<int:account_id>/', manager_views.freeze_account_view, name='freeze_account'),
]
```

**4. Templates (Presentation Layer)**
- HTML files with Django template language
- Display data from views
- Handle user input forms
- Extend base templates for consistency
- Include template tags and filters

**Example:**
```html
{% extends 'base.html' %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<div class="dashboard">
    <h1>Welcome, {{ user.username }}!</h1>
    
    <div class="info-box">
        <h3>Account Balance</h3>
        <p>₹{{ account.balance|floatformat:2 }}</p>
    </div>
    
    <div class="info-box">
        <h3>Account Number</h3>
        <p>{{ account.account_number }}</p>
    </div>
    
    {% if account.status == 'FROZEN' %}
        <div class="alert alert-error">
            Your account is frozen. Please contact support.
        </div>
    {% endif %}
</div>
{% endblock %}
```

---

### Role-Based Access Control

**Implementation Methods:**

**1. Decorators**
```python
from django.contrib.auth.decorators import login_required

@login_required  # Must be logged in
def dashboard_view(request):
    # View logic
    pass

# Custom decorator for managers
def manager_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'manager_profile'):
            messages.error(request, 'Unauthorized access.')
            return redirect('users:login')
        return view_func(request, *args, **kwargs)
    return wrapper

@manager_required  # Must be a manager
def manager_dashboard_view(request):
    # Manager view logic
    pass
```

**2. Conditional Checks in Views**
```python
def dashboard_view(request):
    # Check if user is admin
    if request.user.is_superuser:
        return redirect('bank:admin_dashboard')
    
    # Check if user is manager
    if hasattr(request.user, 'manager_profile'):
        return redirect('bank:manager_dashboard')
    
    # Regular customer dashboard
    account = Account.objects.get(user=request.user)
    return render(request, 'bank/dashboard.html', {'account': account})
```

**3. Template-Level Conditionals**
```html
<nav>
    {% if user.manager_profile %}
        <!-- Manager Navigation -->
        <a href="{% url 'bank:manager_dashboard' %}">Manager Dashboard</a>
        <a href="{% url 'bank:manager_users' %}">Users</a>
        <a href="{% url 'bank:manager_accounts' %}">Accounts</a>
    {% else %}
        <!-- Customer Navigation -->
        <a href="{% url 'bank:dashboard' %}">Dashboard</a>
        <a href="{% url 'bank:deposit' %}">Deposit</a>
        <a href="{% url 'bank:withdraw' %}">Withdraw</a>
    {% endif %}
</nav>
```

**4. Query Filtering**
```python
# Customers can only see their own data
account = Account.objects.get(user=request.user)
transactions = Transaction.objects.filter(account=account)

# Managers can see all data
all_accounts = Account.objects.all()
all_transactions = Transaction.objects.all()
```


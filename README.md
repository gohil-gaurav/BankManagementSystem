# 🏦 Bank Management System

A modern, full-featured bank management system built with Django featuring separate interfaces for customers, bank managers, and administrators. Includes responsive design, transaction management, account freezing, and comprehensive reporting.

![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Responsive](https://img.shields.io/badge/Responsive-Yes-brightgreen.svg)

## ✨ Features

### 👤 For Customers:
- ✅ User registration and authentication
- ✅ Automatic bank account creation with unique account numbers
- ✅ Deposit and withdraw money with real-time balance updates
- ✅ View detailed transaction history
- ✅ Account status monitoring (Active/Frozen)
- ✅ Responsive dashboard for all devices
- ✅ Indian Rupee (₹) currency support

### 👨‍💼 For Bank Managers:
- ✅ Separate manager authentication system
- ✅ Comprehensive dashboard with system statistics
- ✅ User management (view, search, monitor)
- ✅ Account management (view, freeze, unfreeze)
- ✅ Transaction monitoring and approval system
- ✅ Pending transaction approvals
- ✅ Detailed reports and analytics
- ✅ Action audit trail logging
- ✅ Advanced search functionality

### 🔐 For Administrators (Superuser):
- ✅ Enhanced Django admin panel with custom actions
- ✅ Special admin dashboard in the main UI
- ✅ Complete system overview with statistics
- ✅ Bulk operations on accounts and transactions
- ✅ Visual status indicators and warnings
- ✅ Direct access to all system data

## 🛠️ Technology Stack

| Category | Technology |
|----------|-----------|
| **Backend** | Django 4.2.7 |
| **Frontend** | Django Templates, HTML5, CSS3, JavaScript |
| **Database** | SQLite3 (Development) |
| **Design** | Black & White Minimalist Theme |
| **Responsive** | Mobile-first design with CSS Grid & Flexbox |
| **Currency** | Indian Rupee (₹) |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd BankManagementSystem
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create demo data (Optional but Recommended):**
   ```bash
   python setup_demo_data.py
   ```
   This creates:
   - 1 Admin account
   - 1 Manager account
   - 5 Customer accounts with initial balances

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   - Main site: http://127.0.0.1:8000/
   - Django Admin: http://127.0.0.1:8000/admin/

---

## 🔐 Demo Credentials

After running `setup_demo_data.py`, you can use these credentials:

### 👑 Administrator (Superuser)
- **URL:** http://127.0.0.1:8000/users/login/
- **Username:** `admin`
- **Password:** `admin123`
- **Access:** Full system access, admin dashboard, Django admin panel

### 👨‍💼 Bank Manager
- **URL:** http://127.0.0.1:8000/bank/manager/login/
- **Username:** `manager`
- **Password:** `manager123`
- **Employee ID:** EMP001
- **Access:** Manager dashboard, user/account management, reports

### 👤 Demo Customers
- **URL:** http://127.0.0.1:8000/users/login/

| Username | Password | Initial Balance |
|----------|----------|----------------|
| `john_doe` | `john123` | ₹50,000.00 |
| `sarah_smith` | `sarah123` | ₹75,000.00 |
| `mike_wilson` | `mike123` | ₹30,000.00 |
| `emma_brown` | `emma123` | ₹1,00,000.00 |
| `david_jones` | `david123` | ₹25,000.00 |

> **Note:** If you don't run `setup_demo_data.py`, you'll need to create accounts manually using Django commands or the registration pages.

## 📖 Usage Guide

### 🎯 For Customers

#### Registration
1. Visit: http://127.0.0.1:8000/users/register/
2. Fill in username, email, and password
3. Account is created automatically with a unique account number

#### Login & Features
1. Visit: http://127.0.0.1:8000/users/login/
2. Use your credentials to access the dashboard
3. Available features:
   - **Dashboard:** View account balance, account number, and status
   - **Deposit:** Add money to your account
   - **Withdraw:** Withdraw money (with balance validation)
   - **Transactions:** View complete transaction history

---

### 💼 For Bank Managers

#### Create Manager Account

**Option 1 - Web Registration:**
```
Visit: http://127.0.0.1:8000/bank/manager/register/
Fill in: Username, Email, Password, Employee ID, Phone
```

**Option 2 - Management Command:**
```bash
python manage.py create_manager <username> <password> <employee_id>
```

#### Login & Features
1. Visit: http://127.0.0.1:8000/bank/manager/login/
2. Use manager credentials
3. Available features:
   - **Dashboard:** System statistics and overview
   - **Users:** View and search all customers
   - **Accounts:** View, freeze, and unfreeze accounts
   - **Transactions:** Monitor all transactions
   - **Approvals:** Approve/reject pending transactions
   - **Reports:** Generate system reports

---

### 🔧 For Administrators

#### Access Admin Dashboard
1. Login with superuser credentials at: http://127.0.0.1:8000/users/login/
2. Automatically redirected to admin dashboard
3. Features:
   - Complete system overview
   - View all users, accounts, transactions
   - Manager action logs
   - Quick links to Django admin panel

#### Django Admin Panel
1. Visit: http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Features:
   - Enhanced interface with custom actions
   - Bulk operations (approve/reject transactions, freeze accounts)
   - Visual status indicators
   - Advanced filtering and search

## 📁 Project Structure

```
BankManagementSystem/
├── 📄 manage.py                      # Django management script
├── 📄 setup_demo_data.py            # Demo data creation script
├── 📄 requirements.txt               # Python dependencies
├── 📄 README.md                      # Project documentation
├── 📄 .gitignore                     # Git ignore rules
├── 🗄️ db.sqlite3                     # SQLite database
│
├── 📁 config/                        # Project configuration
│   ├── settings.py                  # Django settings
│   ├── urls.py                      # Main URL configuration
│   ├── production_settings.py       # Production settings
│   ├── asgi.py                      # ASGI configuration
│   └── wsgi.py                      # WSGI configuration
│
├── 📁 apps/                          # Django applications
│   ├── 📁 users/                    # User authentication app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   │
│   └── 📁 bank/                     # Banking operations app
│       ├── models.py                # Account, Transaction, Manager models
│       ├── views.py                 # Customer views
│       ├── manager_views.py         # Manager-specific views
│       ├── forms.py                 # Customer forms
│       ├── manager_forms.py         # Manager forms
│       ├── admin.py                 # Enhanced admin configuration
│       ├── urls.py                  # URL routing
│       └── 📁 management/
│           └── 📁 commands/
│               └── create_manager.py
│
├── 📁 templates/                     # HTML templates
│   ├── base.html                    # Base template with navigation
│   ├── home.html                    # Landing page
│   ├── 📁 users/                    # User templates
│   │   ├── login.html
│   │   └── register.html
│   └── 📁 bank/                     # Banking templates
│       ├── dashboard.html
│       ├── admin_dashboard.html
│       ├── transactions.html
│       ├── deposit.html
│       ├── withdraw.html
│       └── manager_*.html           # 14 manager templates
│
└── 📁 static/                        # Static files
    ├── 📁 css/
    │   └── style.css                # Main stylesheet (27KB, responsive)
    └── 📁 js/
        └── main.js                  # JavaScript functionality
```

## 🗄️ Database Models

### User (Django built-in)
Extended with OneToOne relationships to Account and BankManager

### Account
| Field | Type | Description |
|-------|------|-------------|
| `user` | OneToOne | Link to User model |
| `account_number` | CharField | Unique 10-digit (ACC + 7 digits) |
| `balance` | DecimalField | Current account balance |
| `status` | CharField | ACTIVE or FROZEN |
| `created_at` | DateTimeField | Account creation timestamp |
| `last_activity` | DateTimeField | Last transaction timestamp |

### Transaction
| Field | Type | Description |
|-------|------|-------------|
| `account` | ForeignKey | Link to Account |
| `transaction_type` | CharField | DEPOSIT or WITHDRAWAL |
| `amount` | DecimalField | Transaction amount |
| `balance_after` | DecimalField | Balance after transaction |
| `status` | CharField | COMPLETED, PENDING, or FAILED |
| `timestamp` | DateTimeField | Transaction timestamp |
| `description` | TextField | Optional description |

### BankManager
| Field | Type | Description |
|-------|------|-------------|
| `user` | OneToOne | Link to User model |
| `employee_id` | CharField | Unique employee identifier |
| `phone` | CharField | Contact number |
| `created_at` | DateTimeField | Manager creation timestamp |

### ManagerAction
| Field | Type | Description |
|-------|------|-------------|
| `manager` | ForeignKey | Link to BankManager |
| `action_type` | CharField | Type of action performed |
| `target_user` | ForeignKey | User affected by action |
| `target_account` | ForeignKey | Account affected by action |
| `description` | TextField | Action details |
| `timestamp` | DateTimeField | Action timestamp |

## 🎨 Key Features Explained

### 🔄 Automatic Account Creation
When a user registers, a Django signal automatically creates a bank account with a unique account number (format: ACC + 7 random digits).

### ❄️ Account Freezing
- Managers can freeze accounts to prevent all transactions
- Frozen accounts display warning banners
- Deposit and withdraw buttons are disabled
- All transaction attempts are blocked

### ✅ Transaction Validation
- **Withdrawals:** Check for sufficient balance before processing
- **Frozen Accounts:** Cannot perform any transactions
- **Atomic Operations:** All transactions use database-level atomicity
- **Real-time Updates:** Balance updates immediately after transactions

### 📝 Manager Action Logging
All manager actions (freeze, unfreeze, approve, reject) are logged in the ManagerAction model for complete audit trails.

### 📱 Responsive Design
Fully responsive with breakpoints for:
- **Desktop:** 1024px+ (3-4 column grids)
- **Tablet:** 768px - 1024px (2 column grids)
- **Mobile:** 480px - 768px (single column, stacked)
- **Small Mobile:** <480px (compact spacing)

### 🔒 Security Features
- Password hashing (Django default PBKDF2)
- CSRF protection on all forms
- Login required decorators
- Separate authentication for managers
- Admin-only views with permission checks

## ⚙️ Configuration

### Settings
Key settings in `config/settings.py`:
```python
DEBUG = True  # Set to False in production
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']  # Add your domain in production
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/bank/dashboard/'
```

### Database
**Development:** SQLite3 (`db.sqlite3`)

**Production:** Update `DATABASES` in settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🔧 Development Commands

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

### Creating Superuser
```bash
python manage.py createsuperuser
```

### Creating Manager
```bash
python manage.py create_manager <username> <password> <employee_id>
```

### Setup Demo Data
```bash
python setup_demo_data.py
```

---

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings.py
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Use environment variables for sensitive data
- [ ] Set up a production database (PostgreSQL recommended)
- [ ] Configure static files serving
- [ ] Set up HTTPS with SSL certificate
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Configure a reverse proxy (Nginx, Apache)
- [ ] Set up proper logging
- [ ] Enable database backups

### Environment Variables
Create a `.env` file for sensitive data:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Example Deployment with Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

---

## 📸 Screenshots

### Customer Dashboard
- View account balance and details
- Quick access to deposit and withdraw
- Recent transaction history

### Manager Dashboard
- System statistics overview
- User and account management
- Transaction monitoring

### Admin Dashboard
- Complete system overview
- All users, accounts, and transactions
- Manager action logs

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 style guide for Python code
- Write meaningful commit messages
- Add comments for complex logic
- Update documentation for new features
- Test your changes thoroughly

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🐛 Known Issues

- None at the moment

---

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Submit a pull request
- Contact the maintainers

---

## 🙏 Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- Inspired by modern banking systems
- Created for educational and demonstration purposes

---

## 📊 Project Stats

- **Lines of Code:** ~5,000+
- **Python Files:** 20+
- **HTML Templates:** 22
- **CSS:** Responsive design with 27KB stylesheet
- **Database Models:** 5 main models
- **Views:** 30+ views (customer + manager + admin)
- **Features:** 40+ features across all user types

---

## 🔮 Future Enhancements

- [ ] Email notifications for transactions
- [ ] Two-factor authentication (2FA)
- [ ] Transaction receipts (PDF generation)
- [ ] Account statements
- [ ] Loan management system
- [ ] Credit/Debit card management
- [ ] Mobile app (React Native/Flutter)
- [ ] API endpoints (REST/GraphQL)
- [ ] Real-time notifications (WebSockets)
- [ ] Multi-currency support
- [ ] Advanced analytics and charts

---

## 📚 Documentation

For more detailed documentation, see:
- [Django Documentation](https://docs.djangoproject.com/)
- [Python Documentation](https://docs.python.org/)

---

**Made with ❤️ using Django**

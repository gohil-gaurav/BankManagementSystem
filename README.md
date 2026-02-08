# Bank Management System

A basic bank management system built with Django for learning purposes.

## Features

### For Customers:
- User registration and login
- Automatic bank account creation
- Deposit money
- Withdraw money
- View transaction history
- Dashboard with account details

### For Bank Managers:
- Separate manager login and registration
- View all customer accounts
- Search accounts by number or username
- View detailed account information
- Monitor all transactions
- Statistics dashboard (total accounts, balance, deposits, withdrawals)

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Start the development server:
   ```bash
   python manage.py runserver
   ```

4. Open browser and visit: http://127.0.0.1:8000/

## Login Credentials

### Test Manager Account:
- **URL:** http://127.0.0.1:8000/bank/manager/login/
- **Username:** manager
- **Password:** admin123

### Create New Manager:
- **Web:** http://127.0.0.1:8000/bank/manager/register/
- **Command:** `python manage.py create_manager <username> <password> <employee_id>`

### Regular Users:
- **URL:** http://127.0.0.1:8000/users/login/
- Register new account at: http://127.0.0.1:8000/users/register/

## Project Structure

```
BankManagementSystem/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── config/                 # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── apps/                   # Custom applications
│   ├── users/             # User authentication
│   └── bank/              # Banking operations & manager views
├── templates/             # HTML templates
│   ├── base.html
│   ├── users/
│   └── bank/
└── static/                # CSS, JS, images
    ├── css/
    └── js/
```

## Technology Stack

- Backend: Django 4.2.7
- Frontend: Django Templates, HTML, CSS
- Database: SQLite
- Design: Black & White Theme

## Documentation

- `LOGIN_CREDENTIALS.md` - All login credentials and URLs
- `MANAGER_SETUP.md` - How to create bank managers
- `BANK_MANAGER_FEATURE.md` - Complete manager feature guide

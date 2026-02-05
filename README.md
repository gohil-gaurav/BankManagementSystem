# Bank Management System

A basic bank management system built with Django for learning purposes.

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
│   └── bank/              # Banking operations
├── templates/             # HTML templates
│   ├── base.html
│   ├── users/
│   └── bank/
└── static/                # CSS, JS, images
    ├── css/
    └── js/
```

## Setup Instructions

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```
   python manage.py migrate
   ```

3. Start the development server:
   ```
   python manage.py runserver
   ```

4. Open browser and visit: http://127.0.0.1:8000/

## Features (To be implemented)

- User registration and authentication
- Bank account creation
- Deposit money
- Withdraw money
- View transaction history
- Dashboard with account details

## Technology Stack

- Backend: Django 4.2.7
- Frontend: Django Templates, HTML, CSS
- Database: SQLite

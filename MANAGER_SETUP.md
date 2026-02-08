# Bank Manager Setup Guide

## How to Create a Bank Manager

You have two options to create a bank manager:

### Option 1: Using Management Command (Recommended)

Run this command in your terminal:

```bash
python manage.py create_manager <username> <password> <employee_id> --email <email> --phone <phone>
```

**Example:**
```bash
python manage.py create_manager manager1 manager123 EMP001 --email manager@bank.com --phone 9876543210
```

**Required Arguments:**
- `username` - Username for the manager
- `password` - Password for the manager
- `employee_id` - Unique employee ID (e.g., EMP001)

**Optional Arguments:**
- `--email` - Email address
- `--phone` - Phone number

### Option 2: Using Django Admin Panel

1. Login to Django admin at: `http://127.0.0.1:8000/admin/`
2. Go to "Bank Managers" section
3. Click "Add Bank Manager"
4. First create a User (or select existing user)
5. Enter Employee ID and Phone
6. Save

### Option 3: Using Python Shell

```bash
python manage.py shell
```

Then run:
```python
from django.contrib.auth.models import User
from apps.bank.models import BankManager

# Create user
user = User.objects.create_user(
    username='manager1',
    password='manager123',
    email='manager@bank.com'
)

# Create manager profile
manager = BankManager.objects.create(
    user=user,
    employee_id='EMP001',
    phone='9876543210'
)

print(f"Manager created: {manager}")
```

## Manager Login

Once created, the manager can login at:
- **URL:** `http://127.0.0.1:8000/bank/manager/login/`

## Manager Features

Bank managers can:
- View all customer accounts
- See total statistics (accounts, balance, deposits, withdrawals)
- Search accounts by account number or username
- View detailed account information
- See all transaction history for any account
- View recent transactions across all accounts

## Important Notes

1. **Regular users cannot access manager dashboard** - Only users with BankManager profile can access
2. **Managers cannot perform transactions** - They can only view data
3. **Employee ID must be unique** - Each manager needs a unique employee ID
4. **Managers don't have bank accounts** - Manager users don't get automatic Account creation

## Testing

To test the manager system:

1. Create a manager using one of the methods above
2. Create some regular users and perform transactions
3. Login as manager at `/bank/manager/login/`
4. View the dashboard with all accounts and transactions

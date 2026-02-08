# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Start the Server
```bash
python manage.py runserver
```

### Step 2: Choose Your Login Type

#### Option A: Login as Bank Manager
1. Go to: http://127.0.0.1:8000/bank/manager/login/
2. Enter credentials:
   - Username: `manager`
   - Password: `admin123`
3. You'll see the Manager Dashboard with:
   - Statistics (total accounts, balance, etc.)
   - All customer accounts
   - Recent transactions
   - Search functionality

#### Option B: Create New Manager Account
1. Go to: http://127.0.0.1:8000/bank/manager/register/
2. Fill in the form:
   - Username (choose any)
   - Employee ID (e.g., EMP002, EMP003)
   - Password
3. Click "Register as Manager"

#### Option C: Login as Regular Customer
1. Go to: http://127.0.0.1:8000/users/login/
2. Or register new account: http://127.0.0.1:8000/users/register/
3. You'll see your personal dashboard with:
   - Your account balance
   - Deposit/Withdraw buttons
   - Your transaction history

### Step 3: Test the Features

#### As Manager:
- ✅ View all customer accounts
- ✅ Search for specific accounts
- ✅ Click "View Details" on any account
- ✅ See complete transaction history
- ✅ Monitor statistics

#### As Customer:
- ✅ Deposit money
- ✅ Withdraw money
- ✅ View your transactions
- ✅ Check your balance

## 📋 All URLs at a Glance

| What | URL |
|------|-----|
| Home Page | http://127.0.0.1:8000/ |
| **Manager Login** | http://127.0.0.1:8000/bank/manager/login/ |
| **Manager Register** | http://127.0.0.1:8000/bank/manager/register/ |
| Manager Dashboard | http://127.0.0.1:8000/bank/manager/dashboard/ |
| Customer Login | http://127.0.0.1:8000/users/login/ |
| Customer Register | http://127.0.0.1:8000/users/register/ |
| Customer Dashboard | http://127.0.0.1:8000/bank/dashboard/ |

## 🔑 Test Credentials

### Superuser (Django Admin)
```
URL: http://127.0.0.1:8000/admin/
Username: admin
Password: admin123
```

### Manager Account (Already Created)
```
URL: http://127.0.0.1:8000/bank/manager/login/
Username: manager
Password: admin123
Employee ID: EMP001
```

### Customer Account (Already Created)
```
URL: http://127.0.0.1:8000/users/login/
Username: gaurav
Password: gaurav123
```

### Create Your Own Manager
**Web Form:**
- Visit: http://127.0.0.1:8000/bank/manager/register/

**Command Line:**
```bash
python manage.py create_manager john john123 EMP002
```

## ❓ Common Questions

### Q: I can't login as manager, what should I do?
**A:** Make sure you're using:
1. Correct URL: `/bank/manager/login/` (not `/users/login/`)
2. Correct credentials: username=`manager`, password=`admin123`
3. If still not working, reset password:
   ```bash
   python manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username='manager'); u.set_password('admin123'); u.save()"
   ```

### Q: Where is the "create manager account" button?
**A:** Go to: http://127.0.0.1:8000/bank/manager/register/
Or click "Register here" link on the manager login page.

### Q: Can regular users access manager dashboard?
**A:** No, only users with BankManager profile can access. Regular users will see an error message.

### Q: Can managers deposit/withdraw money?
**A:** No, managers can only VIEW data. They cannot perform transactions. Managers are staff, not customers.

### Q: How do I create multiple managers?
**A:** Use the registration page or command line:
```bash
python manage.py create_manager manager2 pass123 EMP002
python manage.py create_manager manager3 pass123 EMP003
```

## 🎨 Design

- Black & White Theme
- Clean, minimal interface
- No emojis
- Indian Rupees (₹) currency
- Responsive tables and cards

## 📚 Need More Help?

Check these files:
- `LOGIN_CREDENTIALS.md` - All credentials and URLs
- `MANAGER_SETUP.md` - Detailed manager setup
- `BANK_MANAGER_FEATURE.md` - Complete feature documentation
- `README.md` - Project overview

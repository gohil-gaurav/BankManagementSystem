# Testing Guide - Bank Management System

## ✅ Your System is Now Running!

The server is running at: **http://127.0.0.1:8000/**

---

## Step-by-Step Testing

### 1. Test Login Page
1. Open browser and go to: http://127.0.0.1:8000/
2. You should be redirected to: http://127.0.0.1:8000/users/login/
3. You'll see a clean login form

### 2. Test Registration
1. Click "Register here" link at the bottom
2. Fill in the form:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `testpass123`
   - Confirm Password: `testpass123`
3. Click "Register"
4. You should be:
   - Automatically logged in
   - See success message: "Welcome testuser! Your account has been created."
   - Redirected to dashboard
   - See your account number (e.g., ACC1234567)
   - See balance: $0.00

### 3. Test Dashboard
After registration, you should see:
- Welcome message with your username
- Account Number (auto-generated)
- Current Balance ($0.00)
- Account Created date
- Quick action buttons (Deposit, Withdraw, Transactions)
- Recent Transactions section (empty for now)

### 4. Test Navigation
Click on the navigation links:
- **Dashboard** - Shows account overview
- **Deposit** - Placeholder page (will implement next)
- **Withdraw** - Placeholder page (will implement next)
- **Transactions** - Shows transaction history (empty for now)
- **Logout** - Logs you out and redirects to login

### 5. Test Logout
1. Click "Logout" in navigation
2. You should see: "You have been logged out successfully."
3. Redirected to login page

### 6. Test Login (Existing User)
1. Go to login page
2. Enter credentials:
   - Username: `testuser`
   - Password: `testpass123`
3. Click "Login"
4. You should see: "Welcome back, testuser!"
5. Redirected to dashboard

### 7. Test Admin Panel
1. Go to: http://127.0.0.1:8000/admin/
2. Login with:
   - Username: `admin`
   - Password: `admin`
3. Click "Accounts" - You should see 2 accounts:
   - admin's account (ACC6183327)
   - testuser's account (new account number)
4. Click "Transactions" - Empty for now

---

## What's Working Now

✅ User Registration
✅ User Login/Logout
✅ Auto Account Creation (via signal)
✅ Dashboard with account info
✅ Navigation bar
✅ Message system (success/error alerts)
✅ Protected routes (must login to access dashboard)
✅ Clean, responsive UI

---

## What's Next

In the next step, we'll implement:
- Deposit functionality (add money)
- Withdraw functionality (remove money with validation)
- Transaction recording
- Real-time balance updates

---

## Common Issues

### Issue: "Page not found (404)"
**Solution:** Make sure the server is running (`python manage.py runserver`)

### Issue: "CSRF verification failed"
**Solution:** Make sure `{% csrf_token %}` is in all forms (already added)

### Issue: "Account has no attribute 'account'"
**Solution:** The signal should auto-create accounts. If not, create manually:
```python
python manage.py shell
from django.contrib.auth.models import User
from apps.bank.models import Account
user = User.objects.get(username='testuser')
Account.objects.create(user=user)
```

### Issue: Password validation errors
**Solution:** Django requires:
- At least 8 characters
- Not entirely numeric
- Not too common (like "password123")

---

## Database Check

To verify everything in the database:

```bash
python manage.py shell
```

```python
# Check users
from django.contrib.auth.models import User
print(f"Total users: {User.objects.count()}")
for user in User.objects.all():
    print(f"- {user.username}")

# Check accounts
from apps.bank.models import Account
print(f"\nTotal accounts: {Account.objects.count()}")
for account in Account.objects.all():
    print(f"- {account.account_number} ({account.user.username}): ${account.balance}")

# Check transactions
from apps.bank.models import Transaction
print(f"\nTotal transactions: {Transaction.objects.count()}")
```

---

## Screenshots to Expect

### Login Page
- Clean form with username and password
- Link to registration
- Blue "Login" button

### Registration Page
- Form with username, email, password, confirm password
- Validation hints below fields
- Link to login

### Dashboard
- Welcome message
- 3 colorful info boxes (Account Number, Balance, Created Date)
- Quick action buttons
- Recent transactions table (empty initially)

---

## Next Step Preview

**STEP 4 - Deposit & Withdraw Functionality**

We'll build:
1. Deposit form (enter amount, add to balance)
2. Withdraw form (enter amount, validate sufficient funds)
3. Transaction recording (every deposit/withdraw creates a Transaction)
4. Balance updates (atomic operations)
5. Success/error messages
6. Transaction history display

Ready to continue? 🚀

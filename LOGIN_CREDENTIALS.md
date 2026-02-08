# Login Credentials

## Django Admin (Superuser)

**Login URL:** http://127.0.0.1:8000/admin/

**Superuser Account:**
- **Username:** admin
- **Password:** admin123

**What you can do:**
- Access Django admin panel
- Manage all users, accounts, transactions
- Create/edit/delete any data
- View all database records

## Bank Manager Login

**Login URL:** http://127.0.0.1:8000/bank/manager/login/

**Test Manager Account:**
- **Username:** manager
- **Password:** admin123
- **Employee ID:** EMP001

## How to Create New Manager Account

### Option 1: Web Registration (Easy)
1. Go to: http://127.0.0.1:8000/bank/manager/register/
2. Fill in the form:
   - Username (required)
   - Email (optional)
   - Employee ID (required, must be unique, e.g., EMP002)
   - Phone (optional)
   - Password (required)
   - Confirm Password (required)
3. Click "Register as Manager"
4. You'll be automatically logged in

### Option 2: Command Line
```bash
python manage.py create_manager <username> <password> <employee_id>
```

**Example:**
```bash
python manage.py create_manager john john123 EMP002
```

## Regular User Login

**Login URL:** http://127.0.0.1:8000/users/login/

**Test Customer Account:**
- **Username:** gaurav
- **Password:** gaurav123

**What you can do:**
- View your account balance
- Deposit money
- Withdraw money
- View your transaction history
- Access customer dashboard

**Note:** This is a regular customer account with a bank account automatically created.

## URLs Summary

| Page | URL |
|------|-----|
| Home | http://127.0.0.1:8000/ |
| User Login | http://127.0.0.1:8000/users/login/ |
| User Register | http://127.0.0.1:8000/users/register/ |
| Manager Login | http://127.0.0.1:8000/bank/manager/login/ |
| Manager Register | http://127.0.0.1:8000/bank/manager/register/ |
| Manager Dashboard | http://127.0.0.1:8000/bank/manager/dashboard/ |
| User Dashboard | http://127.0.0.1:8000/bank/dashboard/ |
| Django Admin | http://127.0.0.1:8000/admin/ |

## Troubleshooting

### Cannot Login as Manager?
1. Make sure you're using the correct URL: `/bank/manager/login/`
2. Use credentials: username=`manager`, password=`admin123`
3. If still not working, reset password:
   ```bash
   python manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username='manager'); u.set_password('admin123'); u.save(); print('Password reset')"
   ```

### Want to Create Another Manager?
- Use the web registration: http://127.0.0.1:8000/bank/manager/register/
- Or use command: `python manage.py create_manager newmanager pass123 EMP002`

### Regular User Trying to Access Manager Dashboard?
- Regular users cannot access manager pages
- You'll see error: "You are not authorized as a bank manager"
- Use the correct login page for your account type

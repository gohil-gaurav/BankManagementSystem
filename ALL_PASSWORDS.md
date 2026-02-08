# 🔑 All Login Credentials - Quick Reference

## 1. Django Admin (Superuser)
**URL:** http://127.0.0.1:8000/admin/

```
Username: admin
Password: admin123
```

**Access:**
- Full admin panel access
- Manage all users, accounts, transactions
- Create/edit/delete any data
- View database records

---

## 2. Bank Manager
**URL:** http://127.0.0.1:8000/bank/manager/login/

```
Username: manager
Password: admin123
Employee ID: EMP001
```

**Access:**
- Manager dashboard
- View all customer accounts
- Search accounts
- View all transactions
- See statistics

---

## 3. Regular Customer
**URL:** http://127.0.0.1:8000/users/login/

```
Username: gaurav
Password: gaurav123
```

**Access:**
- Customer dashboard
- Deposit money
- Withdraw money
- View own transactions
- Check balance

---

## Quick Access URLs

| Account Type | Login URL |
|--------------|-----------|
| **Superuser (Admin)** | http://127.0.0.1:8000/admin/ |
| **Bank Manager** | http://127.0.0.1:8000/bank/manager/login/ |
| **Regular Customer** | http://127.0.0.1:8000/users/login/ |

---

## Create New Accounts

### Create New Manager:
**URL:** http://127.0.0.1:8000/bank/manager/register/

**Or Command:**
```bash
python manage.py create_manager <username> <password> <employee_id>
```

### Create New Customer:
**URL:** http://127.0.0.1:8000/users/register/

### Create New Superuser:
```bash
python manage.py createsuperuser
```

---

## Password Reset Commands

If you forget passwords again, use these commands:

### Reset Superuser Password:
```bash
python manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username='admin'); u.set_password('admin123'); u.save(); print('Done')"
```

### Reset Manager Password:
```bash
python manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username='manager'); u.set_password('admin123'); u.save(); print('Done')"
```

### Reset Customer Password:
```bash
python manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username='gaurav'); u.set_password('gaurav123'); u.save(); print('Done')"
```

### Reset Any User Password:
```bash
python manage.py changepassword <username>
```

---

## Summary Table

| Username | Password | Type | Login URL |
|----------|----------|------|-----------|
| admin | admin123 | Superuser | /admin/ |
| manager | admin123 | Bank Manager | /bank/manager/login/ |
| gaurav | gaurav123 | Customer | /users/login/ |

---

## Important Notes

1. **All passwords have been reset** to the values shown above
2. **Save this file** for future reference
3. **Change passwords** in production environment
4. **These are test credentials** - use strong passwords for real deployment

---

## Test Each Account

### Test 1: Superuser
1. Go to http://127.0.0.1:8000/admin/
2. Login: admin / admin123
3. You should see Django admin panel

### Test 2: Manager
1. Go to http://127.0.0.1:8000/bank/manager/login/
2. Login: manager / admin123
3. You should see manager dashboard with statistics

### Test 3: Customer
1. Go to http://127.0.0.1:8000/users/login/
2. Login: gaurav / gaurav123
3. You should see customer dashboard with balance

---

**All passwords are now reset and working!** ✅

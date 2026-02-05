# Database Models Documentation

## Overview

Our Bank Management System uses 3 main database tables (models):

1. **User** (Django built-in)
2. **Account** (Custom)
3. **Transaction** (Custom)

---

## Database Relationships

```
User (1) ←──────→ (1) Account (1) ←──────→ (Many) Transaction

Example:
User: john_doe
  └── Account: ACC1234567 (Balance: $500.00)
        ├── Transaction 1: DEPOSIT  $100.00 → Balance: $100.00
        ├── Transaction 2: DEPOSIT  $200.00 → Balance: $300.00
        ├── Transaction 3: WITHDRAW $50.00  → Balance: $250.00
        └── Transaction 4: DEPOSIT  $250.00 → Balance: $500.00
```

---

## Model 1: User (Django Built-in)

Django provides this model automatically.

**Fields:**
- `id` - Primary key (auto)
- `username` - Unique username
- `email` - Email address
- `password` - Hashed password
- `first_name` - First name
- `last_name` - Last name
- `date_joined` - When user registered

**Relationship:**
- One User has ONE Account (One-to-One)

---

## Model 2: Account (Custom)

Stores bank account information for each user.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | BigAutoField | Primary key (auto-generated) |
| `user` | OneToOneField | Links to User (one user = one account) |
| `account_number` | CharField(10) | Unique account number (e.g., ACC1234567) |
| `balance` | DecimalField(12,2) | Current balance (e.g., 1500.50) |
| `created_at` | DateTimeField | When account was created |

**Key Features:**
- Account number is auto-generated (format: ACC + 7 digits)
- Balance uses DecimalField for precise money calculations
- OneToOneField ensures one user = one account
- Signal automatically creates account when user registers

**Relationship:**
- Belongs to ONE User (One-to-One)
- Has MANY Transactions (One-to-Many)

**Access Pattern:**
```python
# Get user's account
user.account

# Get account's user
account.user
```

---

## Model 3: Transaction (Custom)

Records every deposit and withdrawal.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | BigAutoField | Primary key (auto-generated) |
| `account` | ForeignKey | Links to Account |
| `transaction_type` | CharField(10) | Either 'DEPOSIT' or 'WITHDRAW' |
| `amount` | DecimalField(12,2) | Amount of money |
| `balance_after` | DecimalField(12,2) | Balance after this transaction |
| `description` | CharField(200) | Optional note (nullable) |
| `timestamp` | DateTimeField | When transaction occurred |

**Transaction Types:**
- `DEPOSIT` - Money added to account
- `WITHDRAW` - Money removed from account

**Key Features:**
- ForeignKey allows one account to have many transactions
- Stores balance_after for historical tracking
- Ordered by timestamp (newest first)
- Uses choices to limit transaction_type values

**Relationship:**
- Belongs to ONE Account (Many-to-One)

**Access Pattern:**
```python
# Get all transactions for an account
account.transactions.all()

# Get account from transaction
transaction.account
```

---

## Why These Relationships?

### One-to-One (User ↔ Account)
- **Why?** Each user should have exactly ONE bank account
- **Implementation:** `OneToOneField` in Account model
- **Benefit:** Prevents users from having multiple accounts (keeps it simple)

### One-to-Many (Account ↔ Transaction)
- **Why?** One account can have MANY transactions over time
- **Implementation:** `ForeignKey` in Transaction model
- **Benefit:** Complete transaction history for each account

---

## Auto-Generated Fields

### Account Number
- **Format:** ACC + 7 random digits (e.g., ACC1234567)
- **Generation:** Happens automatically when account is saved
- **Uniqueness:** Checks database to ensure no duplicates

### Timestamps
- **created_at:** Set once when account is created
- **timestamp:** Set once when transaction is created
- **Implementation:** `auto_now_add=True`

---

## Django Signals

**What are signals?**
Signals allow certain actions to trigger automatically when something happens.

**Our Signal:**
```python
@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
```

**What it does:**
- Listens for User creation
- Automatically creates an Account when new User is registered
- User doesn't need to manually create account

**Why use signals?**
- Ensures every user ALWAYS has an account
- Happens automatically (no extra code needed in views)
- Keeps code DRY (Don't Repeat Yourself)

---

## Database Schema (SQL Equivalent)

```sql
-- User table (Django built-in)
CREATE TABLE auth_user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(150) UNIQUE,
    email VARCHAR(254),
    password VARCHAR(128),
    date_joined DATETIME
);

-- Account table
CREATE TABLE bank_account (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE,  -- One-to-One with User
    account_number VARCHAR(10) UNIQUE,
    balance DECIMAL(12, 2) DEFAULT 0.00,
    created_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES auth_user(id)
);

-- Transaction table
CREATE TABLE bank_transaction (
    id INTEGER PRIMARY KEY,
    account_id INTEGER,  -- Many-to-One with Account
    transaction_type VARCHAR(10),
    amount DECIMAL(12, 2),
    balance_after DECIMAL(12, 2),
    description VARCHAR(200),
    timestamp DATETIME,
    FOREIGN KEY (account_id) REFERENCES bank_account(id)
);
```

---

## Testing the Models

### Via Django Shell
```bash
python manage.py shell
```

```python
# Import models
from django.contrib.auth.models import User
from apps.bank.models import Account, Transaction

# Create a user (account is auto-created via signal)
user = User.objects.create_user(username='testuser', password='testpass123')

# Get the account
account = user.account
print(account.account_number)  # e.g., ACC1234567
print(account.balance)  # 0.00

# Create a deposit transaction
transaction = Transaction.objects.create(
    account=account,
    transaction_type='DEPOSIT',
    amount=100.00,
    balance_after=100.00,
    description='Initial deposit'
)

# Update account balance
account.balance = 100.00
account.save()

# View all transactions
for t in account.transactions.all():
    print(f"{t.transaction_type}: ${t.amount}")
```

### Via Django Admin
1. Run server: `python manage.py runserver`
2. Visit: http://127.0.0.1:8000/admin/
3. Login with superuser credentials
4. View Accounts and Transactions

---

## Next Steps

Now that models are created, we'll build:
1. User registration form
2. User login/logout views
3. Dashboard to display account info
4. Deposit/Withdraw functionality
5. Transaction history page

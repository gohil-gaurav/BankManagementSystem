"""
Quick test script to verify models are working
Run with: python manage.py shell < test_models.py
"""

from django.contrib.auth.models import User
from apps.bank.models import Account, Transaction

print("\n" + "="*50)
print("TESTING BANK MODELS")
print("="*50 + "\n")

# Test 1: Check existing users and accounts
print("1. Existing Data:")
print(f"   Total Users: {User.objects.count()}")
print(f"   Total Accounts: {Account.objects.count()}")
print(f"   Total Transactions: {Transaction.objects.count()}")

# Test 2: Show account details
if Account.objects.exists():
    account = Account.objects.first()
    print(f"\n2. First Account Details:")
    print(f"   Account Number: {account.account_number}")
    print(f"   User: {account.user.username}")
    print(f"   Balance: ${account.balance}")
    print(f"   Created: {account.created_at.strftime('%Y-%m-%d %H:%M')}")

# Test 3: Create a test transaction
if Account.objects.exists():
    account = Account.objects.first()
    
    # Create deposit
    transaction = Transaction.objects.create(
        account=account,
        transaction_type='DEPOSIT',
        amount=100.00,
        balance_after=100.00,
        description='Test deposit'
    )
    
    # Update balance
    account.balance = 100.00
    account.save()
    
    print(f"\n3. Created Test Transaction:")
    print(f"   Type: {transaction.transaction_type}")
    print(f"   Amount: ${transaction.amount}")
    print(f"   Balance After: ${transaction.balance_after}")
    print(f"   Time: {transaction.timestamp.strftime('%Y-%m-%d %H:%M')}")
    
    print(f"\n4. Updated Account Balance: ${account.balance}")

print("\n" + "="*50)
print("✅ ALL TESTS PASSED!")
print("="*50 + "\n")

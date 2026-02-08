#!/usr/bin/env python
"""
Setup script to create demo users and managers for the Bank Management System.
Run this after migrations to populate the database with test data.
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.bank.models import Account, Transaction, BankManager
from decimal import Decimal

def create_demo_data():
    print("=" * 60)
    print("Setting up demo data for Bank Management System")
    print("=" * 60)
    
    # Create superuser (admin)
    print("\n1. Creating superuser...")
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@bank.com',
            password='admin123',
            first_name='System',
            last_name='Administrator'
        )
        print("   ✓ Superuser created: admin / admin123")
    else:
        print("   ✓ Superuser already exists")
    
    # Create bank manager
    print("\n2. Creating bank manager...")
    if not User.objects.filter(username='manager').exists():
        manager_user = User.objects.create_user(
            username='manager',
            email='manager@bank.com',
            password='manager123',
            first_name='John',
            last_name='Manager'
        )
        BankManager.objects.create(
            user=manager_user,
            employee_id='EMP001',
            phone='+1234567890'
        )
        print("   ✓ Manager created: manager / manager123 (Employee ID: EMP001)")
    else:
        print("   ✓ Manager already exists")
    
    # Create demo customers
    print("\n3. Creating demo customers...")
    
    customers = [
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'john123',
            'first_name': 'John',
            'last_name': 'Doe',
            'initial_balance': Decimal('50000.00')
        },
        {
            'username': 'sarah_smith',
            'email': 'sarah@example.com',
            'password': 'sarah123',
            'first_name': 'Sarah',
            'last_name': 'Smith',
            'initial_balance': Decimal('75000.00')
        },
        {
            'username': 'mike_wilson',
            'email': 'mike@example.com',
            'password': 'mike123',
            'first_name': 'Mike',
            'last_name': 'Wilson',
            'initial_balance': Decimal('30000.00')
        },
        {
            'username': 'emma_brown',
            'email': 'emma@example.com',
            'password': 'emma123',
            'first_name': 'Emma',
            'last_name': 'Brown',
            'initial_balance': Decimal('100000.00')
        },
        {
            'username': 'david_jones',
            'email': 'david@example.com',
            'password': 'david123',
            'first_name': 'David',
            'last_name': 'Jones',
            'initial_balance': Decimal('25000.00')
        }
    ]
    
    for customer_data in customers:
        username = customer_data['username']
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=customer_data['username'],
                email=customer_data['email'],
                password=customer_data['password'],
                first_name=customer_data['first_name'],
                last_name=customer_data['last_name']
            )
            
            # Update account balance
            account = Account.objects.get(user=user)
            account.balance = customer_data['initial_balance']
            account.save()
            
            # Create initial deposit transaction
            Transaction.objects.create(
                account=account,
                transaction_type='DEPOSIT',
                amount=customer_data['initial_balance'],
                balance_after=customer_data['initial_balance'],
                status='COMPLETED',
                description='Initial deposit'
            )
            
            print(f"   ✓ Customer created: {username} / {customer_data['password']} (Balance: ₹{customer_data['initial_balance']:,.2f})")
        else:
            print(f"   ✓ Customer {username} already exists")
    
    print("\n" + "=" * 60)
    print("Demo data setup complete!")
    print("=" * 60)
    
    # Print summary
    print("\n📊 SUMMARY:")
    print(f"   Total Users: {User.objects.count()}")
    print(f"   Total Accounts: {Account.objects.count()}")
    print(f"   Total Managers: {BankManager.objects.count()}")
    print(f"   Total Transactions: {Transaction.objects.count()}")
    print(f"   Total Balance: ₹{sum(acc.balance for acc in Account.objects.all()):,.2f}")
    
    print("\n🔐 LOGIN CREDENTIALS:")
    print("\n   ADMIN (Superuser):")
    print("   URL: http://127.0.0.1:8000/users/login/")
    print("   Username: admin")
    print("   Password: admin123")
    
    print("\n   MANAGER:")
    print("   URL: http://127.0.0.1:8000/bank/manager/login/")
    print("   Username: manager")
    print("   Password: manager123")
    
    print("\n   CUSTOMERS:")
    print("   URL: http://127.0.0.1:8000/users/login/")
    for customer in customers:
        print(f"   - {customer['username']} / {customer['password']}")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    try:
        create_demo_data()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have run migrations first:")
        print("   python manage.py migrate")

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random


class BankManager(models.Model):
    """
    Bank Manager Model
    - Identifies which users are bank managers
    - Managers can view all accounts and transactions
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='manager_profile'
    )
    employee_id = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Manager: {self.user.username}"
    
    class Meta:
        verbose_name = 'Bank Manager'
        verbose_name_plural = 'Bank Managers'


class Account(models.Model):
    """
    Bank Account Model
    - Each user has ONE account (One-to-One relationship)
    - Stores account number, balance, and creation date
    """
    
    # Account Status Choices
    ACTIVE = 'ACTIVE'
    FROZEN = 'FROZEN'
    
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (FROZEN, 'Frozen'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='account'
    )
    # WHY OneToOneField? Because one user = one account (not multiple accounts)
    # on_delete=CASCADE means: if user is deleted, delete their account too
    # related_name='account' means: we can access account via user.account
    
    account_number = models.CharField(
        max_length=10, 
        unique=True, 
        editable=False
    )
    # WHY unique=True? No two accounts can have same number
    # WHY editable=False? We auto-generate it, users can't change it
    
    balance = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00
    )
    # WHY DecimalField? For precise money calculations (not float!)
    # max_digits=12 means: up to 9,999,999,999.99 (10 digits + 2 decimals)
    # decimal_places=2 means: always 2 decimal places (cents)
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=ACTIVE
    )
    # Account can be ACTIVE or FROZEN by manager
    
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True means: automatically set when account is created
    
    last_activity = models.DateTimeField(auto_now=True)
    # Tracks last activity on account
    
    def __str__(self):
        return f"{self.user.username} - {self.account_number}"
    
    def save(self, *args, **kwargs):
        """
        Override save method to auto-generate account number
        This runs every time we save an Account
        """
        if not self.account_number:  # Only generate if account_number is empty
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)
    
    def generate_account_number(self):
        """
        Generate a unique 10-digit account number
        Format: ACC + 7 random digits (e.g., ACC1234567)
        """
        while True:
            # Generate random 7-digit number
            number = 'ACC' + str(random.randint(1000000, 9999999))
            
            # Check if this number already exists
            if not Account.objects.filter(account_number=number).exists():
                return number  # Return if unique
            # If not unique, loop continues and generates new number
    
    class Meta:
        ordering = ['-created_at']  # Newest accounts first



class Transaction(models.Model):
    """
    Transaction Model
    - Records every deposit and withdrawal
    - Linked to Account (One account can have many transactions)
    """
    
    # Transaction type choices
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'
    
    TRANSACTION_TYPES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAW, 'Withdraw'),
    ]
    # WHY choices? Limits transaction_type to only these two values
    # Prevents typos like "depositt" or "withdra"
    
    # Transaction status choices
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    COMPLETED = 'COMPLETED'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (COMPLETED, 'Completed'),
    ]
    
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    # WHY ForeignKey? One account can have MANY transactions (One-to-Many)
    # related_name='transactions' means: account.transactions.all() gets all transactions
    
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES
    )
    # Stores either 'DEPOSIT' or 'WITHDRAW'
    
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    # The amount of money deposited or withdrawn
    
    balance_after = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    # WHY store balance_after? So we can show historical balance at each transaction
    # Example: "On Jan 1, you withdrew $50, balance was $450"
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=COMPLETED
    )
    # Transaction status for approval workflow
    
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    # Optional note about the transaction
    # blank=True means: form can be submitted without this field
    # null=True means: database can store NULL for this field
    
    timestamp = models.DateTimeField(auto_now_add=True)
    # When the transaction happened
    
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_transactions'
    )
    # Manager who approved the transaction
    
    approval_note = models.TextField(blank=True, null=True)
    # Manager's note when approving/rejecting
    
    def __str__(self):
        return f"{self.transaction_type} - ₹{self.amount} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-timestamp']  # Newest transactions first
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'


class ManagerAction(models.Model):
    """
    Log of all manager actions for audit trail
    """
    ACTION_TYPES = [
        ('FREEZE_ACCOUNT', 'Freeze Account'),
        ('UNFREEZE_ACCOUNT', 'Unfreeze Account'),
        ('APPROVE_TRANSACTION', 'Approve Transaction'),
        ('REJECT_TRANSACTION', 'Reject Transaction'),
        ('VIEW_USER', 'View User Details'),
        ('VIEW_ACCOUNT', 'View Account Details'),
    ]
    
    manager = models.ForeignKey(
        BankManager,
        on_delete=models.CASCADE,
        related_name='actions'
    )
    action_type = models.CharField(max_length=30, choices=ACTION_TYPES)
    target_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='manager_actions_on'
    )
    target_account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    target_transaction = models.ForeignKey(
        Transaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    note = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.manager.user.username} - {self.action_type} - {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Manager Action'
        verbose_name_plural = 'Manager Actions'


# Signal to auto-create account when user registers
@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    """
    Automatically create an Account when a new User is created
    This is called a 'signal' - it listens for User creation
    """
    if created:  # Only run when a NEW user is created (not on updates)
        # Don't create account for managers
        if not hasattr(instance, 'manager_profile'):
            Account.objects.create(user=instance)
            # Creates account with default balance of 0.00


@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    """
    Save the account whenever user is saved
    """
    if hasattr(instance, 'account'):  # Check if user has an account
        instance.account.save()

from django.contrib import admin
from .models import Account, Transaction, BankManager, ManagerAction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """
    Customize how Account appears in Django admin panel
    """
    list_display = ['account_number', 'user', 'balance', 'created_at']
    # Columns to show in the list view
    
    list_filter = ['created_at']
    # Add filter sidebar for creation date
    
    search_fields = ['account_number', 'user__username']
    # Allow searching by account number or username
    
    readonly_fields = ['account_number', 'created_at']
    # These fields can't be edited in admin (auto-generated)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Customize how Transaction appears in Django admin panel
    """
    list_display = ['account', 'transaction_type', 'amount', 'balance_after', 'timestamp']
    # Columns to show in the list view
    
    list_filter = ['transaction_type', 'timestamp']
    # Add filters for transaction type and date
    
    search_fields = ['account__account_number', 'account__user__username']
    # Allow searching by account number or username
    
    readonly_fields = ['timestamp']
    # Timestamp can't be edited
    
    date_hierarchy = 'timestamp'
    # Add date navigation at the top


@admin.register(BankManager)
class BankManagerAdmin(admin.ModelAdmin):
    """
    Customize how BankManager appears in Django admin panel
    """
    list_display = ['user', 'employee_id', 'phone', 'created_at']
    search_fields = ['user__username', 'employee_id']
    readonly_fields = ['created_at']


@admin.register(ManagerAction)
class ManagerActionAdmin(admin.ModelAdmin):
    """
    Customize how ManagerAction appears in Django admin panel
    """
    list_display = ['manager', 'action_type', 'target_user', 'timestamp']
    list_filter = ['action_type', 'timestamp']
    search_fields = ['manager__user__username', 'target_user__username']
    readonly_fields = ['timestamp']

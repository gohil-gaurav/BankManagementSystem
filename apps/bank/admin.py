from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Account, Transaction, BankManager, ManagerAction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """
    Customize how Account appears in Django admin panel
    """
    list_display = ['account_number', 'user_link', 'balance_display', 'status_display', 'created_at', 'last_activity', 'action_buttons']
    list_filter = ['status', 'created_at']
    search_fields = ['account_number', 'user__username', 'user__email']
    readonly_fields = ['account_number', 'created_at', 'last_activity', 'transaction_count', 'total_deposits', 'total_withdrawals']
    
    fieldsets = (
        ('Account Information', {
            'fields': ('account_number', 'user', 'balance', 'status')
        }),
        ('Statistics', {
            'fields': ('transaction_count', 'total_deposits', 'total_withdrawals')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_activity')
        }),
    )
    
    def user_link(self, obj):
        """Link to user detail page"""
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    def balance_display(self, obj):
        """Display balance with currency"""
        return format_html('<strong>₹{:,.2f}</strong>', float(obj.balance))
    balance_display.short_description = 'Balance'
    balance_display.admin_order_field = 'balance'
    
    def status_display(self, obj):
        """Display status with color"""
        if obj.status == 'ACTIVE':
            color = '#4ade80'
            icon = '●'
        else:
            color = '#ef4444'
            icon = '●'
        return format_html('<span style="color: {};">{} {}</span>', color, icon, obj.status)
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status'
    
    def action_buttons(self, obj):
        """Add freeze/unfreeze buttons"""
        if obj.status == 'ACTIVE':
            return format_html(
                '<a class="button" href="{}">Freeze Account</a>',
                reverse('admin:bank_account_freeze', args=[obj.pk])
            )
        else:
            return format_html(
                '<a class="button" href="{}">Unfreeze Account</a>',
                reverse('admin:bank_account_unfreeze', args=[obj.pk])
            )
    action_buttons.short_description = 'Actions'
    
    def transaction_count(self, obj):
        """Count of transactions"""
        return obj.transactions.count()
    transaction_count.short_description = 'Total Transactions'
    
    def total_deposits(self, obj):
        """Total deposit amount"""
        total = sum(t.amount for t in obj.transactions.filter(transaction_type='DEPOSIT', status='COMPLETED'))
        return format_html('₹{:,.2f}', float(total))
    total_deposits.short_description = 'Total Deposits'
    
    def total_withdrawals(self, obj):
        """Total withdrawal amount"""
        total = sum(t.amount for t in obj.transactions.filter(transaction_type='WITHDRAW', status='COMPLETED'))
        return format_html('₹{:,.2f}', float(total))
    total_withdrawals.short_description = 'Total Withdrawals'
    
    actions = ['freeze_accounts', 'unfreeze_accounts']
    
    def freeze_accounts(self, request, queryset):
        """Bulk freeze accounts"""
        updated = queryset.update(status='FROZEN')
        self.message_user(request, f'{updated} account(s) have been frozen.')
    freeze_accounts.short_description = 'Freeze selected accounts'
    
    def unfreeze_accounts(self, request, queryset):
        """Bulk unfreeze accounts"""
        updated = queryset.update(status='ACTIVE')
        self.message_user(request, f'{updated} account(s) have been unfrozen.')
    unfreeze_accounts.short_description = 'Unfreeze selected accounts'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Customize how Transaction appears in Django admin panel
    """
    list_display = ['transaction_id', 'account_link', 'user_name', 'transaction_type_display', 'amount_display', 'balance_after_display', 'status_display', 'timestamp', 'approved_by_display']
    list_filter = ['transaction_type', 'status', 'timestamp']
    search_fields = ['account__account_number', 'account__user__username', 'description']
    readonly_fields = ['timestamp', 'transaction_details']
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('account', 'transaction_type', 'amount', 'balance_after', 'status')
        }),
        ('Details', {
            'fields': ('description', 'approved_by', 'approval_note')
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
        ('Summary', {
            'fields': ('transaction_details',),
            'classes': ('collapse',)
        }),
    )
    
    def transaction_id(self, obj):
        """Display transaction ID"""
        return f'#{obj.id}'
    transaction_id.short_description = 'ID'
    
    def account_link(self, obj):
        """Link to account"""
        url = reverse('admin:bank_account_change', args=[obj.account.id])
        return format_html('<a href="{}">{}</a>', url, obj.account.account_number)
    account_link.short_description = 'Account'
    
    def user_name(self, obj):
        """Display user name"""
        return obj.account.user.username
    user_name.short_description = 'Customer'
    
    def transaction_type_display(self, obj):
        """Display transaction type with icon"""
        if obj.transaction_type == 'DEPOSIT':
            return format_html('<span style="color: #4ade80;">↓ Deposit</span>')
        else:
            return format_html('<span style="color: #ef4444;">↑ Withdraw</span>')
    transaction_type_display.short_description = 'Type'
    
    def amount_display(self, obj):
        """Display amount with currency"""
        if obj.amount >= 50000:
            return format_html('<strong style="color: #fbbf24;">₹{:,.2f} ⚠️</strong>', float(obj.amount))
        return format_html('<strong>₹{:,.2f}</strong>', float(obj.amount))
    amount_display.short_description = 'Amount'
    amount_display.admin_order_field = 'amount'
    
    def balance_after_display(self, obj):
        """Display balance after transaction"""
        return format_html('₹{:,.2f}', float(obj.balance_after))
    balance_after_display.short_description = 'Balance After'
    
    def status_display(self, obj):
        """Display status with color"""
        colors = {
            'COMPLETED': '#4ade80',
            'PENDING': '#fbbf24',
            'APPROVED': '#4ade80',
            'REJECTED': '#ef4444',
        }
        color = colors.get(obj.status, '#888')
        return format_html('<span style="color: {};">● {}</span>', color, obj.status)
    status_display.short_description = 'Status'
    
    def approved_by_display(self, obj):
        """Display who approved"""
        if obj.approved_by:
            return obj.approved_by.username
        return '—'
    approved_by_display.short_description = 'Approved By'
    
    def transaction_details(self, obj):
        """Show detailed transaction info"""
        html = f"""
        <div style="background: #f5f5f5; padding: 15px; border-radius: 5px;">
            <h3>Transaction Details</h3>
            <table style="width: 100%;">
                <tr><td><strong>Transaction ID:</strong></td><td>#{obj.id}</td></tr>
                <tr><td><strong>Account:</strong></td><td>{obj.account.account_number}</td></tr>
                <tr><td><strong>Customer:</strong></td><td>{obj.account.user.username}</td></tr>
                <tr><td><strong>Type:</strong></td><td>{obj.transaction_type}</td></tr>
                <tr><td><strong>Amount:</strong></td><td>₹{obj.amount:,.2f}</td></tr>
                <tr><td><strong>Balance After:</strong></td><td>₹{obj.balance_after:,.2f}</td></tr>
                <tr><td><strong>Status:</strong></td><td>{obj.status}</td></tr>
                <tr><td><strong>Date:</strong></td><td>{obj.timestamp.strftime('%B %d, %Y %H:%M')}</td></tr>
                <tr><td><strong>Description:</strong></td><td>{obj.description or '—'}</td></tr>
                {f'<tr><td><strong>Approved By:</strong></td><td>{obj.approved_by.username}</td></tr>' if obj.approved_by else ''}
                {f'<tr><td><strong>Approval Note:</strong></td><td>{obj.approval_note}</td></tr>' if obj.approval_note else ''}
            </table>
        </div>
        """
        return mark_safe(html)
    transaction_details.short_description = 'Transaction Details'
    
    actions = ['approve_transactions', 'reject_transactions']
    
    def approve_transactions(self, request, queryset):
        """Bulk approve transactions"""
        updated = queryset.filter(status='PENDING').update(status='APPROVED', approved_by=request.user)
        self.message_user(request, f'{updated} transaction(s) have been approved.')
    approve_transactions.short_description = 'Approve selected transactions'
    
    def reject_transactions(self, request, queryset):
        """Bulk reject transactions"""
        updated = queryset.filter(status='PENDING').update(status='REJECTED', approved_by=request.user)
        self.message_user(request, f'{updated} transaction(s) have been rejected.')
    reject_transactions.short_description = 'Reject selected transactions'


@admin.register(BankManager)
class BankManagerAdmin(admin.ModelAdmin):
    """
    Customize how BankManager appears in Django admin panel
    """
    list_display = ['user_link', 'employee_id', 'phone', 'created_at', 'total_actions']
    search_fields = ['user__username', 'employee_id', 'phone']
    readonly_fields = ['created_at', 'total_actions', 'recent_actions_display']
    
    fieldsets = (
        ('Manager Information', {
            'fields': ('user', 'employee_id', 'phone')
        }),
        ('Statistics', {
            'fields': ('total_actions', 'created_at')
        }),
        ('Recent Actions', {
            'fields': ('recent_actions_display',),
            'classes': ('collapse',)
        }),
    )
    
    def user_link(self, obj):
        """Link to user"""
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    def total_actions(self, obj):
        """Count of actions performed"""
        return obj.actions.count()
    total_actions.short_description = 'Total Actions'
    
    def recent_actions_display(self, obj):
        """Show recent actions"""
        actions = obj.actions.all()[:10]
        if not actions:
            return 'No actions yet'
        
        html = '<table style="width: 100%; border-collapse: collapse;">'
        html += '<tr style="background: #f5f5f5;"><th>Action</th><th>Target</th><th>Date</th></tr>'
        for action in actions:
            html += f'<tr><td>{action.action_type}</td><td>{action.target_user.username if action.target_user else "—"}</td><td>{action.timestamp.strftime("%b %d, %Y %H:%M")}</td></tr>'
        html += '</table>'
        return mark_safe(html)
    recent_actions_display.short_description = 'Recent Actions'


@admin.register(ManagerAction)
class ManagerActionAdmin(admin.ModelAdmin):
    """
    Customize how ManagerAction appears in Django admin panel
    """
    list_display = ['action_id', 'manager_name', 'action_type_display', 'target_user_link', 'target_account_link', 'timestamp']
    list_filter = ['action_type', 'timestamp']
    search_fields = ['manager__user__username', 'target_user__username', 'note']
    readonly_fields = ['timestamp', 'action_details']
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Action Information', {
            'fields': ('manager', 'action_type', 'note')
        }),
        ('Targets', {
            'fields': ('target_user', 'target_account', 'target_transaction')
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
        ('Details', {
            'fields': ('action_details',),
            'classes': ('collapse',)
        }),
    )
    
    def action_id(self, obj):
        """Display action ID"""
        return f'#{obj.id}'
    action_id.short_description = 'ID'
    
    def manager_name(self, obj):
        """Display manager name"""
        return obj.manager.user.username
    manager_name.short_description = 'Manager'
    
    def action_type_display(self, obj):
        """Display action type with color"""
        colors = {
            'FREEZE_ACCOUNT': '#ef4444',
            'UNFREEZE_ACCOUNT': '#4ade80',
            'APPROVE_TRANSACTION': '#4ade80',
            'REJECT_TRANSACTION': '#ef4444',
            'VIEW_USER': '#888',
            'VIEW_ACCOUNT': '#888',
        }
        color = colors.get(obj.action_type, '#888')
        return format_html('<span style="color: {};">● {}</span>', color, obj.action_type.replace('_', ' ').title())
    action_type_display.short_description = 'Action Type'
    
    def target_user_link(self, obj):
        """Link to target user"""
        if obj.target_user:
            url = reverse('admin:auth_user_change', args=[obj.target_user.id])
            return format_html('<a href="{}">{}</a>', url, obj.target_user.username)
        return '—'
    target_user_link.short_description = 'Target User'
    
    def target_account_link(self, obj):
        """Link to target account"""
        if obj.target_account:
            url = reverse('admin:bank_account_change', args=[obj.target_account.id])
            return format_html('<a href="{}">{}</a>', url, obj.target_account.account_number)
        return '—'
    target_account_link.short_description = 'Target Account'
    
    def action_details(self, obj):
        """Show detailed action info"""
        html = f"""
        <div style="background: #f5f5f5; padding: 15px; border-radius: 5px;">
            <h3>Action Details</h3>
            <table style="width: 100%;">
                <tr><td><strong>Action ID:</strong></td><td>#{obj.id}</td></tr>
                <tr><td><strong>Manager:</strong></td><td>{obj.manager.user.username} (EMP: {obj.manager.employee_id})</td></tr>
                <tr><td><strong>Action Type:</strong></td><td>{obj.action_type.replace('_', ' ').title()}</td></tr>
                <tr><td><strong>Date & Time:</strong></td><td>{obj.timestamp.strftime('%B %d, %Y %H:%M:%S')}</td></tr>
                {f'<tr><td><strong>Target User:</strong></td><td>{obj.target_user.username}</td></tr>' if obj.target_user else ''}
                {f'<tr><td><strong>Target Account:</strong></td><td>{obj.target_account.account_number}</td></tr>' if obj.target_account else ''}
                {f'<tr><td><strong>Target Transaction:</strong></td><td>#{obj.target_transaction.id}</td></tr>' if obj.target_transaction else ''}
                <tr><td><strong>Note:</strong></td><td>{obj.note or '—'}</td></tr>
            </table>
        </div>
        """
        return mark_safe(html)
    action_details.short_description = 'Action Details'

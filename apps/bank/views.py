from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import DepositForm, WithdrawForm
from .models import Transaction


@login_required
def dashboard_view(request):
    """
    Dashboard View - Shows account information
    @login_required ensures only logged-in users can access
    """
    from django.db.models import Sum
    
    # If user is a manager, redirect to manager dashboard
    if hasattr(request.user, 'manager_profile'):
        return redirect('bank:manager_dashboard')
    
    # If user is superuser (admin), show admin dashboard with all features
    if request.user.is_superuser:
        return admin_dashboard_view(request)
    
    account = request.user.account
    
    # Check if account is frozen
    if account.status == 'FROZEN':
        messages.warning(request, 'Your account has been frozen. Please contact the bank for assistance.')
    
    recent_transactions = account.transactions.all()[:5]  # Last 5 transactions
    
    # Calculate statistics for fintech dashboard
    total_deposits = account.transactions.filter(
        transaction_type='DEPOSIT',
        status='COMPLETED'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_withdrawals = account.transactions.filter(
        transaction_type='WITHDRAW',
        status='COMPLETED'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    transaction_count = account.transactions.count()
    
    context = {
        'account': account,
        'recent_transactions': recent_transactions,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'transaction_count': transaction_count,
    }
    return render(request, 'bank/dashboard.html', context)


@login_required
def admin_dashboard_view(request):
    """
    Admin Dashboard View - Shows all system information and management features
    Only accessible to superusers
    """
    from django.contrib.auth.models import User
    from django.db.models import Sum, Count, Q
    from .models import Account, Transaction, BankManager, ManagerAction
    
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('bank:dashboard')
    
    # Get all statistics
    total_users = User.objects.exclude(manager_profile__isnull=False).count()
    total_accounts = Account.objects.count()
    total_balance = Account.objects.aggregate(Sum('balance'))['balance__sum'] or 0
    total_transactions = Transaction.objects.count()
    
    # Transaction statistics
    total_deposits = Transaction.objects.filter(
        transaction_type='DEPOSIT', 
        status='COMPLETED'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_withdrawals = Transaction.objects.filter(
        transaction_type='WITHDRAW', 
        status='COMPLETED'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Account statistics
    active_accounts = Account.objects.filter(status='ACTIVE').count()
    frozen_accounts = Account.objects.filter(status='FROZEN').count()
    
    # Transaction status
    pending_transactions = Transaction.objects.filter(status='PENDING').count()
    completed_transactions = Transaction.objects.filter(status='COMPLETED').count()
    
    # Recent data
    recent_users = User.objects.exclude(manager_profile__isnull=False).order_by('-date_joined')[:10]
    recent_accounts = Account.objects.select_related('user').order_by('-created_at')[:10]
    recent_transactions = Transaction.objects.select_related('account__user').order_by('-timestamp')[:20]
    
    # Large transactions (>= 50000)
    large_transactions = Transaction.objects.filter(amount__gte=50000).order_by('-timestamp')[:10]
    
    # Manager statistics
    total_managers = BankManager.objects.count()
    recent_manager_actions = ManagerAction.objects.select_related(
        'manager__user', 'target_user', 'target_account'
    ).order_by('-timestamp')[:15]
    
    # Get all accounts for management
    all_accounts = Account.objects.select_related('user').all()
    
    # Get all users for management
    all_users = User.objects.exclude(manager_profile__isnull=False).select_related('account')
    
    context = {
        'is_admin': True,
        'total_users': total_users,
        'total_accounts': total_accounts,
        'total_balance': total_balance,
        'total_transactions': total_transactions,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'active_accounts': active_accounts,
        'frozen_accounts': frozen_accounts,
        'pending_transactions': pending_transactions,
        'completed_transactions': completed_transactions,
        'recent_users': recent_users,
        'recent_accounts': recent_accounts,
        'recent_transactions': recent_transactions,
        'large_transactions': large_transactions,
        'total_managers': total_managers,
        'recent_manager_actions': recent_manager_actions,
        'all_accounts': all_accounts,
        'all_users': all_users,
    }
    
    return render(request, 'bank/admin_dashboard.html', context)


@login_required
def deposit_view(request):
    """
    Deposit View - Add money to account
    Uses atomic transaction to ensure data consistency
    """
    account = request.user.account
    
    # Check if account is frozen
    if account.status == 'FROZEN':
        messages.error(request, 'Your account is frozen. You cannot perform transactions. Please contact the bank.')
        return redirect('bank:dashboard')
    
    if request.method == 'POST':
        form = DepositForm(request.POST)
        
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data.get('description', 'Deposit')
            
            # Use atomic transaction to ensure all-or-nothing operation
            with transaction.atomic():
                # Update account balance
                account.balance += amount
                account.save()
                
                # Create transaction record
                Transaction.objects.create(
                    account=account,
                    transaction_type='DEPOSIT',
                    amount=amount,
                    balance_after=account.balance,
                    description=description or 'Deposit'
                )
            
            # Show success message
            messages.success(
                request,
                f'Successfully deposited ₹{amount}. New balance: ₹{account.balance}'
            )
            
            # Redirect to dashboard
            return redirect('bank:dashboard')
    else:
        form = DepositForm()
    
    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'bank/deposit.html', context)


@login_required
def withdraw_view(request):
    """
    Withdraw View - Remove money from account
    Validates sufficient funds before processing
    """
    account = request.user.account
    
    # Check if account is frozen
    if account.status == 'FROZEN':
        messages.error(request, 'Your account is frozen. You cannot perform transactions. Please contact the bank.')
        return redirect('bank:dashboard')
    
    if request.method == 'POST':
        form = WithdrawForm(request.POST, balance=account.balance)
        
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data.get('description', 'Withdrawal')
            
            # Double-check balance (extra safety)
            if amount > account.balance:
                messages.error(
                    request,
                    f'Insufficient funds. Your current balance is ₹{account.balance}.'
                )
                return redirect('bank:withdraw')
            
            # Use atomic transaction to ensure all-or-nothing operation
            with transaction.atomic():
                # Update account balance
                account.balance -= amount
                account.save()
                
                # Create transaction record
                Transaction.objects.create(
                    account=account,
                    transaction_type='WITHDRAW',
                    amount=amount,
                    balance_after=account.balance,
                    description=description or 'Withdrawal'
                )
            
            # Show success message
            messages.success(
                request,
                f'Successfully withdrew ₹{amount}. New balance: ₹{account.balance}'
            )
            
            # Redirect to dashboard
            return redirect('bank:dashboard')
    else:
        form = WithdrawForm(balance=account.balance)
    
    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'bank/withdraw.html', context)


@login_required
def transactions_view(request):
    """Transaction History View - Shows all transactions"""
    account = request.user.account
    transactions = account.transactions.all()
    
    context = {
        'transactions': transactions,
        'account': account,
    }
    return render(request, 'bank/transactions.html', context)

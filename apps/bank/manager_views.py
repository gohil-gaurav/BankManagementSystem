from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Account, Transaction, BankManager, ManagerAction
from .manager_forms import ManagerRegistrationForm


def manager_required(view_func):
    """
    Decorator to check if user is a manager
    """
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'manager_profile'):
            messages.error(request, 'You are not authorized to access this page.')
            return redirect('users:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def manager_login_view(request):
    """
    Bank Manager Login View
    - Only users with BankManager profile can login here
    """
    if request.user.is_authenticated:
        # Check if user is a manager
        if hasattr(request.user, 'manager_profile'):
            return redirect('bank:manager_dashboard')
        else:
            messages.error(request, 'You are not authorized as a bank manager.')
            logout(request)
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Check if user is a bank manager
                if hasattr(user, 'manager_profile'):
                    login(request, user)
                    messages.success(request, f'Welcome, Manager {username}!')
                    return redirect('bank:manager_dashboard')
                else:
                    messages.error(request, 'You are not authorized as a bank manager.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'bank/manager_login.html', {'form': form})


@login_required(login_url='bank:manager_login')
@manager_required
def manager_dashboard_view(request):
    """
    Bank Manager Dashboard
    - View all accounts and transactions
    - See statistics
    """
    manager = request.user.manager_profile
    
    # Get search query
    search_query = request.GET.get('search', '')
    
    # Get all accounts
    accounts = Account.objects.select_related('user').all()
    
    # Apply search filter
    if search_query:
        accounts = accounts.filter(
            Q(account_number__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )
    
    # Calculate statistics
    total_users = User.objects.exclude(manager_profile__isnull=False).count()
    total_accounts = Account.objects.count()
    total_balance = Account.objects.aggregate(Sum('balance'))['balance__sum'] or 0
    total_transactions = Transaction.objects.count()
    total_deposits = Transaction.objects.filter(transaction_type='DEPOSIT', status='COMPLETED').aggregate(Sum('amount'))['amount__sum'] or 0
    total_withdrawals = Transaction.objects.filter(transaction_type='WITHDRAW', status='COMPLETED').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Pending approvals
    pending_transactions = Transaction.objects.filter(status='PENDING').count()
    
    # Today's transactions
    today = timezone.now().date()
    today_transactions = Transaction.objects.filter(timestamp__date=today).count()
    
    # Get recent transactions (last 10)
    recent_transactions = Transaction.objects.select_related('account__user').all()[:10]
    
    # Frozen accounts count
    frozen_accounts = Account.objects.filter(status='FROZEN').count()
    
    context = {
        'manager': manager,
        'accounts': accounts[:20],  # Limit to 20 for dashboard
        'search_query': search_query,
        'total_users': total_users,
        'total_accounts': total_accounts,
        'total_balance': total_balance,
        'total_transactions': total_transactions,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'pending_transactions': pending_transactions,
        'today_transactions': today_transactions,
        'recent_transactions': recent_transactions,
        'frozen_accounts': frozen_accounts,
    }
    
    return render(request, 'bank/manager_dashboard.html', context)


@login_required(login_url='bank:manager_login')
@manager_required
def manager_users_view(request):
    """
    View all users with supervision
    """
    manager = request.user.manager_profile
    search_query = request.GET.get('search', '')
    
    # Get all users except managers
    users = User.objects.exclude(manager_profile__isnull=False).select_related('account')
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Identify inactive users (no activity in last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    users_data = []
    for user in users:
        last_transaction = Transaction.objects.filter(account__user=user).first()
        is_inactive = False
        if last_transaction:
            is_inactive = last_transaction.timestamp < thirty_days_ago
        elif user.date_joined < thirty_days_ago:
            is_inactive = True
        
        users_data.append({
            'user': user,
            'is_inactive': is_inactive,
            'last_login': user.last_login,
            'has_account': hasattr(user, 'account'),
        })
    
    context = {
        'manager': manager,
        'users_data': users_data,
        'search_query': search_query,
    }
    
    return render(request, 'bank/manager_users.html', context)


@login_required(login_url='bank:manager_login')
@manager_required
def manager_user_detail_view(request, user_id):
    """
    View detailed user profile
    """
    manager = request.user.manager_profile
    user = get_object_or_404(User, id=user_id)
    
    # Log the action
    ManagerAction.objects.create(
        manager=manager,
        action_type='VIEW_USER',
        target_user=user,
        note=f'Viewed user profile: {user.username}'
    )
    
    # Get user's account if exists
    account = None
    transactions = []
    if hasattr(user, 'account'):
        account = user.account
        transactions = account.transactions.all()[:20]
    
    context = {
        'manager': manager,
        'target_user': user,
        'account': account,
        'transactions': transactions,
    }
    
    return render(request, 'bank/manager_user_detail.html', context)


@login_required(login_url='bank:manager_login')
@manager_required
def manager_accounts_view(request):
    """
    View all accounts with monitoring
    """
    manager = request.user.manager_profile
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    accounts = Account.objects.select_related('user').all()
    
    if search_query:
        accounts = accounts.filter(
            Q(account_number__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )
    
    if status_filter:
        accounts = accounts.filter(status=status_filter)
    
    context = {
        'manager': manager,
        'accounts': accounts,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'bank/manager_accounts.html', context)


@login_required(login_url='bank:manager_login')
@manager_required
def manager_account_detail_view(request, account_id):
    """
    View detailed information about a specific account
    """
    manager = request.user.manager_profile
    account = get_object_or_404(Account, id=account_id)
    transactions = account.transactions.all()
    
    # Log the action
    ManagerAction.objects.create(
        manager=manager,
        action_type='VIEW_ACCOUNT',
        target_account=account,
        target_user=account.user,
        note=f'Viewed account details: {account.account_number}'
    )
    
    context = {
        'manager': manager,
        'account': account,
        'transactions': transactions,
    }
    
    return render(request, 'bank/manager_account_detail.html', context)


@login_required(login_url='bank:manager_login')
@manager_required
def manager_freeze_account_view(request, account_id):
    """
    Freeze an account
    """
    manager = request.user.manager_profile
    account = get_object_or_404(Account, id=account_id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        
        if account.status == 'FROZEN':
            messages.warning(request, 'Account is already frozen.')
        else:
            account.status = 'FROZEN'
            account.save()
            
            # Log the action
            ManagerAction.objects.create(
                manager=manager,
                action_type='FREEZE_ACCOUNT',
                target_account=account,
                target_user=account.user,
                note=f'Frozen account: {account.account_number}. Reason: {reason}'
            )
            
            messages.success(request, f'Account {account.account_number} has been frozen.')
        
        return redirect('bank:manager_account_detail', account_id=account.id)
    
    context = {
        'manager': manager,
        'account': account,
    }
    
    return render(request, 'bank/manager_freeze_account.html', context)


@login_required(login_url='bank:manager_login')
@manager_required
def manager_unfreeze_account_view(request, account_id):
    """
    Unfreeze an account
    """
    manager = request.user.manager_profile
    account = get_object_or_404(Account, id=account_id)
    
    if request.method == 'POST':
        if account.status == 'ACTIVE':
            messages.warning(request, 'Account is already active.')
        else:
            account.status = 'ACTIVE'
            account.save()
            
            # Log the action
            ManagerAction.objects.create(
                manager=manager,
                action_type='UNFREEZE_ACCOUNT',
                target_account=account,
                target_user=account.user,
                note=f'Unfrozen account: {account.account_number}'
            )
            
            messages.success(request, f'Account {account.account_number} has been unfrozen.')
        
        return redirect('bank:manager_account_detail', account_id=account.id)
    
    context = {
        'manager': manager,
        'account': account,
    }
    
    return render(request, 'bank/manager_unfreeze_account.html', context)


@login_required(login_url='bank:manager_login')
@manager_required
def manager_transactions_view(request):
    """
    View all transactions with filtering
    """
    manager = request.user.manager_profile
    
    # Get filter parameters
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    transaction_type = request.GET.get('type', '')
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    transactions = Transaction.objects.select_related('account__user').all()
    
    # Apply filters
    if date_from:
        transactions = transactions.filter(timestamp__date__gte=date_from)
    if date_to:
        transactions = transactions.filter(timestamp__date__lte=date_to)
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    if status_filter:
        transactions = transactions.filter(status=status_filter)
    if search_query:
        transactions = transactions.filter(
            Q(account__account_number__icontains=search_query) |
            Q(account__user__username__icontains=search_query)
        )
    
    # Identify large transactions (over 50000)
    large_transactions = transactions.filter(amount__gte=50000)
    
    context = {
        'manager': manager,
        'transactions': transactions[:100],  # Limit to 100
        'large_transactions_count': large_transactions.count(),
        'date_from': date_from,
        'date_to': date_to,
        'transaction_type': transaction_type,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'bank/manager_transactions.html', context)


@login_required(login_url='bank:manager_login')
@manager_required
def manager_pending_approvals_view(request):
    """
    View pending transaction approvals
    """
    manager = request.user.manager_profile
    pending_transactions = Transaction.objects.filter(status='PENDING').select_related('account__user')
    
    context = {
        'manager': manager,
        'pending_transactions': pending_transactions,
    }
    
    return render(request, 'bank/manager_pending_approvals.html', context)


@login_required(login_url='bank:manager_login')
@manager_required
def manager_approve_transaction_view(request, transaction_id):
    """
    Approve a pending transaction
    """
    manager = request.user.manager_profile
    transaction = get_object_or_404(Transaction, id=transaction_id)
    
    if request.method == 'POST':
        note = request.POST.get('note', '')
        
        if transaction.status != 'PENDING':
            messages.warning(request, 'This transaction is not pending approval.')
        else:
            transaction.status = 'APPROVED'
            transaction.approved_by = request.user
            transaction.approval_note = note
            transaction.save()
            
            # Log the action
            ManagerAction.objects.create(
                manager=manager,
                action_type='APPROVE_TRANSACTION',
                target_transaction=transaction,
                target_account=transaction.account,
                target_user=transaction.account.user,
                note=f'Approved transaction #{transaction.id}. Note: {note}'
            )
            
            messages.success(request, f'Transaction #{transaction.id} has been approved.')
        
        return redirect('bank:manager_pending_approvals')
    
    context = {
        'manager': manager,
        'transaction': transaction,
    }
    
    return render(request, 'bank/manager_approve_transaction.html', context)


@login_required(login_url='bank:manager_login')
@manager_required
def manager_reject_transaction_view(request, transaction_id):
    """
    Reject a pending transaction
    """
    manager = request.user.manager_profile
    transaction = get_object_or_404(Transaction, id=transaction_id)
    
    if request.method == 'POST':
        note = request.POST.get('note', '')
        
        if transaction.status != 'PENDING':
            messages.warning(request, 'This transaction is not pending approval.')
        else:
            transaction.status = 'REJECTED'
            transaction.approved_by = request.user
            transaction.approval_note = note
            transaction.save()
            
            # Log the action
            ManagerAction.objects.create(
                manager=manager,
                action_type='REJECT_TRANSACTION',
                target_transaction=transaction,
                target_account=transaction.account,
                target_user=transaction.account.user,
                note=f'Rejected transaction #{transaction.id}. Reason: {note}'
            )
            
            messages.success(request, f'Transaction #{transaction.id} has been rejected.')
        
        return redirect('bank:manager_pending_approvals')
    
    context = {
        'manager': manager,
        'transaction': transaction,
    }
    
    return render(request, 'bank/manager_reject_transaction.html', context)


@login_required(login_url='bank:manager_login')
@manager_required
def manager_reports_view(request):
    """
    Generate and view reports
    """
    manager = request.user.manager_profile
    
    # Daily report
    today = timezone.now().date()
    today_transactions = Transaction.objects.filter(timestamp__date=today, status='COMPLETED')
    today_deposits = today_transactions.filter(transaction_type='DEPOSIT').aggregate(Sum('amount'))['amount__sum'] or 0
    today_withdrawals = today_transactions.filter(transaction_type='WITHDRAW').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Weekly report
    week_ago = timezone.now() - timedelta(days=7)
    week_transactions = Transaction.objects.filter(timestamp__gte=week_ago, status='COMPLETED')
    week_deposits = week_transactions.filter(transaction_type='DEPOSIT').aggregate(Sum('amount'))['amount__sum'] or 0
    week_withdrawals = week_transactions.filter(transaction_type='WITHDRAW').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Monthly report
    month_ago = timezone.now() - timedelta(days=30)
    month_transactions = Transaction.objects.filter(timestamp__gte=month_ago, status='COMPLETED')
    month_deposits = month_transactions.filter(transaction_type='DEPOSIT').aggregate(Sum('amount'))['amount__sum'] or 0
    month_withdrawals = month_transactions.filter(transaction_type='WITHDRAW').aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'manager': manager,
        'today_transactions_count': today_transactions.count(),
        'today_deposits': today_deposits,
        'today_withdrawals': today_withdrawals,
        'week_transactions_count': week_transactions.count(),
        'week_deposits': week_deposits,
        'week_withdrawals': week_withdrawals,
        'month_transactions_count': month_transactions.count(),
        'month_deposits': month_deposits,
        'month_withdrawals': month_withdrawals,
    }
    
    return render(request, 'bank/manager_reports.html', context)


def manager_logout_view(request):
    """
    Manager Logout View
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('bank:manager_login')


def manager_register_view(request):
    """
    Bank Manager Registration View
    - Create new bank manager account
    """
    if request.user.is_authenticated:
        if hasattr(request.user, 'manager_profile'):
            return redirect('bank:manager_dashboard')
    
    if request.method == 'POST':
        form = ManagerRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome Manager {user.username}! Your account has been created.')
            return redirect('bank:manager_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ManagerRegistrationForm()
    
    return render(request, 'bank/manager_register.html', {'form': form})

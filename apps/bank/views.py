from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_view(request):
    """
    Dashboard View - Shows account information
    @login_required ensures only logged-in users can access
    """
    account = request.user.account
    recent_transactions = account.transactions.all()[:5]  # Last 5 transactions
    
    context = {
        'account': account,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'bank/dashboard.html', context)


@login_required
def deposit_view(request):
    """Deposit View - Will be implemented in next step"""
    return render(request, 'bank/deposit.html')


@login_required
def withdraw_view(request):
    """Withdraw View - Will be implemented in next step"""
    return render(request, 'bank/withdraw.html')


@login_required
def transactions_view(request):
    """Transaction History View - Will be implemented in next step"""
    account = request.user.account
    transactions = account.transactions.all()
    
    context = {
        'transactions': transactions,
    }
    return render(request, 'bank/transactions.html', context)

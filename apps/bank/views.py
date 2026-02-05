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
    account = request.user.account
    recent_transactions = account.transactions.all()[:5]  # Last 5 transactions
    
    context = {
        'account': account,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'bank/dashboard.html', context)


@login_required
def deposit_view(request):
    """
    Deposit View - Add money to account
    Uses atomic transaction to ensure data consistency
    """
    account = request.user.account
    
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

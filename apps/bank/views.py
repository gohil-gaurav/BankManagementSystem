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


@login_required
def download_transaction_pdf(request, transaction_id):
    """
    Generate and download PDF receipt for a transaction
    """
    from django.http import HttpResponse
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    from io import BytesIO
    from datetime import datetime
    
    # Get the transaction
    try:
        transaction_obj = Transaction.objects.get(id=transaction_id, account__user=request.user)
    except Transaction.DoesNotExist:
        messages.error(request, 'Transaction not found.')
        return redirect('bank:dashboard')
    
    # Create the PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=6
    )
    
    # Add bank header
    elements.append(Paragraph("Bank Management System", title_style))
    elements.append(Paragraph("Transaction Receipt", heading_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Transaction details
    transaction_type = "Deposit" if transaction_obj.transaction_type == 'DEPOSIT' else "Withdrawal"
    amount_prefix = "+" if transaction_obj.transaction_type == 'DEPOSIT' else "-"
    
    data = [
        ['Transaction ID:', str(transaction_obj.id)],
        ['Account Number:', transaction_obj.account.account_number],
        ['Account Holder:', transaction_obj.account.user.username.title()],
        ['Transaction Type:', transaction_type],
        ['Amount:', f'{amount_prefix}₹{transaction_obj.amount:,.2f}'],
        ['Date & Time:', transaction_obj.timestamp.strftime('%B %d, %Y • %I:%M %p')],
        ['Status:', transaction_obj.status.title()],
        ['Balance After:', f'₹{transaction_obj.balance_after:,.2f}'],
    ]
    
    # Create table
    table = Table(data, colWidths=[2.5*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F1F5F9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1E293B')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_text = f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#94A3B8'),
        alignment=TA_CENTER
    )
    elements.append(Paragraph(footer_text, footer_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("This is a computer-generated receipt and does not require a signature.", footer_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="transaction_{transaction_obj.id}_receipt.pdf"'
    response.write(pdf)
    
    return response

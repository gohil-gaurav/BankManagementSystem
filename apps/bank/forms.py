from django import forms
from decimal import Decimal


class DepositForm(forms.Form):
    """
    Deposit Form - Add money to account
    """
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount to deposit',
            'step': '0.01',
            'min': '0.01'
        }),
        label='Amount',
        help_text='Enter the amount you want to deposit (minimum ₹0.01)'
    )
    
    description = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional description (e.g., Salary, Gift)'
        }),
        label='Description (Optional)'
    )
    
    def clean_amount(self):
        """
        Validate amount is positive and reasonable
        """
        amount = self.cleaned_data.get('amount')
        
        if amount <= 0:
            raise forms.ValidationError('Amount must be greater than zero.')
        
        if amount > Decimal('1000000.00'):
            raise forms.ValidationError('Amount cannot exceed ₹1,000,000.00 per transaction.')
        
        return amount


class WithdrawForm(forms.Form):
    """
    Withdraw Form - Remove money from account
    """
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount to withdraw',
            'step': '0.01',
            'min': '0.01'
        }),
        label='Amount',
        help_text='Enter the amount you want to withdraw (minimum ₹0.01)'
    )
    
    description = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional description (e.g., ATM, Shopping)'
        }),
        label='Description (Optional)'
    )
    
    def __init__(self, *args, **kwargs):
        """
        Accept account balance for validation
        """
        self.balance = kwargs.pop('balance', Decimal('0.00'))
        super().__init__(*args, **kwargs)
    
    def clean_amount(self):
        """
        Validate amount is positive and doesn't exceed balance
        """
        amount = self.cleaned_data.get('amount')
        
        if amount <= 0:
            raise forms.ValidationError('Amount must be greater than zero.')
        
        if amount > self.balance:
            raise forms.ValidationError(
                f'Insufficient funds. Your current balance is ₹{self.balance}.'
            )
        
        if amount > Decimal('1000000.00'):
            raise forms.ValidationError('Amount cannot exceed ₹1,000,000.00 per transaction.')
        
        return amount

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import BankManager


class ManagerRegistrationForm(UserCreationForm):
    """
    Form for registering a new bank manager
    """
    email = forms.EmailField(required=False)
    employee_id = forms.CharField(
        max_length=10,
        required=True,
        help_text='Unique employee ID (e.g., EMP001)'
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        help_text='Contact phone number'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'employee_id', 'phone']
    
    def clean_employee_id(self):
        """
        Validate that employee_id is unique
        """
        employee_id = self.cleaned_data.get('employee_id')
        if BankManager.objects.filter(employee_id=employee_id).exists():
            raise forms.ValidationError('This employee ID is already in use.')
        return employee_id
    
    def save(self, commit=True):
        """
        Save user and create manager profile
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '')
        
        if commit:
            user.save()
            # Create manager profile
            BankManager.objects.create(
                user=user,
                employee_id=self.cleaned_data['employee_id'],
                phone=self.cleaned_data.get('phone', '')
            )
        
        return user

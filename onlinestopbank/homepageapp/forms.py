from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    address = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter your address'}))
    
    class Meta:
        model = User
        fields = ['username', 'email','address', 'password']

class DepositWithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

class BillPaymentForm(forms.Form):
    bill_type = forms.ChoiceField(
        choices=[('1', 'Electricity'), ('2', 'Water'), ('3', 'Gas'),('4', 'Home Rent'),('5', 'LoanRepayment'),('6', 'DTH Reacharge')],  # Correct format: list of tuples
        required=True
    )
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

class TransferForm(forms.Form):
    recipient_account_number = forms.CharField(max_length=10)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)  
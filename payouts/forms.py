from django import forms
from .models import PaymentMethod, WithdrawalRequest, WithdrawalPolicy
import json

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['payment_type', 'account_details', 'is_default']
        widgets = {
            'payment_type': forms.Select(attrs={'class': 'form-select'}),
            'account_details': forms.Textarea(attrs={'class': 'form-control', 'style': 'display:none'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def clean_account_details(self):
        payment_type = self.cleaned_data.get('payment_type')
        account_details = self.cleaned_data.get('account_details')

        if isinstance(account_details, str):
            account_details = json.loads(account_details)

        if payment_type == 'paypal' and not account_details.get('email'):
            raise forms.ValidationError("PayPal email is required.")
        elif payment_type == 'bank_transfer':
            if not all([account_details.get('bank_name'), account_details.get('ifsc_code'), account_details.get('account_number')]):
                raise forms.ValidationError("Bank details (Bank Name, IFSC Code, Account Number) are required.")
        elif payment_type == 'crypto' and not account_details.get('wallet_address'):
            raise forms.ValidationError("Crypto wallet address is required.")
        
        return account_details


class WithdrawalRequestForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['amount', 'payment_method']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['payment_method'].queryset = PaymentMethod.objects.filter(user=user)
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        policy = WithdrawalPolicy.objects.first()
        
        if amount < policy.min_amount:
            raise forms.ValidationError(f'Minimum withdrawal amount is ${policy.min_amount}')
        if amount > policy.max_amount:
            raise forms.ValidationError(f'Maximum withdrawal amount is ${policy.max_amount}')
        
        return amount
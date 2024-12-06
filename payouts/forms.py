from django import forms
from .models import PaymentMethod, WithdrawalRequest, WithdrawalPolicy

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['payment_type', 'account_details']
        widgets = {
            'account_details': forms.JSONField(),
        }

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
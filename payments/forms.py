# forms.py
from django import forms
from subscriptions.models import Subscription

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['payment_date', 'payment_id']  # Include any fields you want

    payment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use date input type for the date picker
        required=True,
    )
    payment_id = forms.CharField(max_length=255, required=True)  # Payment ID field

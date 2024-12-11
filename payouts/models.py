from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class PaymentMethod(models.Model):
    PAYMENT_TYPES = [
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('crypto', 'Cryptocurrency'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    account_details = models.JSONField()  # Stores payment-specific details
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.user.email} - {self.payment_type}"


class WithdrawalRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    reference_id = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.email} - ${self.amount} - {self.status}"

    @property
    def can_be_cancelled(self):
        return self.status == 'pending'

class WithdrawalPolicy(models.Model):
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('10.00'))
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1000.00'))
    processing_time_days = models.PositiveIntegerField(default=3)
    withdrawal_fee = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    
    class Meta:
        verbose_name_plural = 'Withdrawal Policies'
    
    def __str__(self):
        return f"Withdrawal Policy (Min: ${self.min_amount}, Max: ${self.max_amount})"
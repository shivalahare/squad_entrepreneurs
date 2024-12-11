from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from django.db.models import Sum
import uuid

class ReferralProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referral_code = models.CharField(max_length=20, unique=True)
    referred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email}'s Referral Profile"

    def calculate_commission(self, payment_amount):
        try:
            commission = (Decimal(payment_amount) * Decimal('0.001')).quantize(Decimal('0.01'))
            return commission
        except Exception :
            return Decimal('0.00')    




    # def calculate_commission(self, payment_amount):
    #     """Calculate commission for a referred user's payment"""
    #     return (Decimal(payment_amount) * Decimal('0.001')).quantize(Decimal('0.01'))  # 0.1%
    
    # def update_total_earnings(self):
    #     """Recalculate and update total earnings."""
    #     earnings = ReferralEarning.objects.filter(referrer=self.user).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    #     self.total_earnings = earnings
    #     self.save()

class ReferralEarning(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_earnings')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey('payments.Payment', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.referrer.email} earned ${self.amount} from {self.referred_user.email}"
    
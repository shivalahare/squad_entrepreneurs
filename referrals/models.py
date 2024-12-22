from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from django.db.models import Sum
import uuid
from datetime import date

class ReferralProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referral_code = models.CharField(max_length=20, unique=True)
    referred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    todays_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    weekly_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_updated = models.DateField(default=date.today)  # Track last update    
   
    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email}'s Referral Profile"

    def calculate_commission(self, payment_amount, level):
        """
        Calculate commission for a referred user's payment.
        Level 1 gets 30%, Level 2 gets 15%.
        """
        if level == 1:
            commission_rate = Decimal('0.30')  # 30% for direct referrals
        elif level == 2:
            commission_rate = Decimal('0.15')  # 15% for second-level referrals
        else:
            return Decimal('0.00')  # No commission beyond level 2

        try:
            commission = (Decimal(payment_amount) * commission_rate).quantize(Decimal('0.01'))
            return commission
        except Exception:
            return Decimal('0.00')

    def reset_todays_earnings(self):
        """Reset today's earnings to zero."""
        self.todays_earnings = 0
        self.save()

    def reset_weekly_earnings(self):
        """Reset weekly earnings to zero."""
        self.weekly_earnings = 0
        self.save()

    def reset_monthly_earnings(self):
        """Reset monthly earnings to zero."""
        self.monthly_earnings = 0
        self.save()

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
    
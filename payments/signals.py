from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment
from referrals.models import ReferralProfile, ReferralEarning

@receiver(post_save, sender=Payment)
def create_referral_earning(sender, instance, created, **kwargs):
    """Create referral earning when a payment is completed."""
    # Check if the payment is newly created or updated to 'completed'
    if instance.status == 'completed':
        try:
            # Get the referral profile of the user who made the payment
            referral_profile = ReferralProfile.objects.get(user=instance.user)
            
            # If the user was referred by someone
            if referral_profile.referred_by:
                # Calculate commission
                commission = referral_profile.calculate_commission(instance.amount)
                
                # Check if an earning for this payment already exists
                if not ReferralEarning.objects.filter(payment=instance).exists():
                    # Create referral earning
                    ReferralEarning.objects.create(
                        referrer=referral_profile.referred_by,
                        referred_user=instance.user,
                        payment=instance,
                        amount=commission
                    )
                    
                    # Update total earnings for referrer
                    referrer_profile = ReferralProfile.objects.get(user=referral_profile.referred_by)
                    referrer_profile.total_earnings += commission
                    referrer_profile.save()
        except ReferralProfile.DoesNotExist:
            pass

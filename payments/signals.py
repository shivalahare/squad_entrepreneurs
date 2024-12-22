from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment
from referrals.models import ReferralProfile, ReferralEarning
from decimal import Decimal

@receiver(post_save, sender=Payment)
def create_referral_earning(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        try:
            # Get the referral profile of the user who made the payment
            referral_profile = ReferralProfile.objects.get(user=instance.user)
            
            # Level 1: Direct referrer
            if referral_profile.referred_by:
                level_1_referrer = referral_profile.referred_by
                level_1_commission = referral_profile.calculate_commission(instance.amount, level=1)

                if not ReferralEarning.objects.filter(payment=instance, referrer=level_1_referrer).exists():
                    ReferralEarning.objects.create(
                        referrer=level_1_referrer,
                        referred_user=instance.user,
                        payment=instance,
                        amount=level_1_commission
                    )

                    # Update all earnings for level 1 referrer
                    level_1_referrer_profile = ReferralProfile.objects.get(user=level_1_referrer)
                    level_1_referrer_profile.total_earnings += level_1_commission
                    level_1_referrer_profile.todays_earnings += level_1_commission
                    level_1_referrer_profile.weekly_earnings += level_1_commission
                    level_1_referrer_profile.monthly_earnings += level_1_commission
                    level_1_referrer_profile.save()

            # Level 2: Second-level referrer
            if referral_profile.referred_by:
                level_1_referrer_profile = ReferralProfile.objects.filter(user=referral_profile.referred_by).first()
                if level_1_referrer_profile and level_1_referrer_profile.referred_by:
                    level_2_referrer = level_1_referrer_profile.referred_by
                    level_2_commission = referral_profile.calculate_commission(instance.amount, level=2)

                    if not ReferralEarning.objects.filter(payment=instance, referrer=level_2_referrer).exists():
                        ReferralEarning.objects.create(
                            referrer=level_2_referrer,
                            referred_user=instance.user,
                            payment=instance,
                            amount=level_2_commission
                        )

                        # Update all earnings for level 2 referrer
                        level_2_referrer_profile = ReferralProfile.objects.get(user=level_2_referrer)
                        level_2_referrer_profile.total_earnings += level_2_commission
                        level_2_referrer_profile.todays_earnings += level_2_commission
                        level_2_referrer_profile.weekly_earnings += level_2_commission
                        level_2_referrer_profile.monthly_earnings += level_2_commission
                        level_2_referrer_profile.save()

        except ReferralProfile.DoesNotExist:
            pass

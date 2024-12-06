from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import ReferralProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_referral_profile(sender, instance, created, **kwargs):
    """
    Create a ReferralProfile for every new user and handle referral relationships
    based on query parameters.
    """
    if created:  # Skip superusers # Only create the profile for newly created users
        # Create a referral profile for the user
        referral_profile = ReferralProfile.objects.get_or_create(user=instance)

        # Handle referral logic from query parameters (if applicable)
        request = kwargs.get('request')  # Django doesn't pass request in post_save
        if request and request.GET.get('ref'):  # Check if ref code exists
            referral_code = request.GET.get('ref')
            try:
                referrer_profile = ReferralProfile.objects.get(referral_code=referral_code)
                referral_profile.referred_by = referrer_profile.user
                referral_profile.save()
            except ReferralProfile.DoesNotExist:
                pass  # If the referral code is invalid, do nothing

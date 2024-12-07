from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import ReferralProfile

@receiver(user_signed_up)
def handle_referral_code_on_signup(user, **kwargs):
    """
    Handle referral code during signup. If no referral code is provided, create 
    a ReferralProfile without a referrer.
    """
    # Get the request object
    request = kwargs.get('request')
    if not request:
        return  # Exit if no request object is available

    # Extract the referral code from the query parameters
    referral_code = request.GET.get('ref')

    # Create or update the user's ReferralProfile
    referral_profile, created = ReferralProfile.objects.get_or_create(user=user)

    if referral_code:  # Handle referral logic if a code is present
        try:
            # Find the referrer's ReferralProfile using the referral code
            referrer_profile = ReferralProfile.objects.get(referral_code=referral_code)
            referral_profile.referred_by = referrer_profile.user  # Set the referrer
            referral_profile.save()
        except ReferralProfile.DoesNotExist:
            # If the referral code is invalid, log it or skip
            pass
    else:
        # No referral code, just save the user's ReferralProfile
        referral_profile.save()

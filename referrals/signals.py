from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import ReferralProfile

@receiver(user_signed_up)
def handle_referral_code_on_signup(request, user, **kwargs):
    """
    Handle referral code during the signup process.
    """
    referral_code = request.GET.get('ref')  # Extract referral code from query parameters
    if referral_code:
        try:
            # Find the referrer's ReferralProfile using the referral code
            referrer_profile = ReferralProfile.objects.get(referral_code=referral_code)
            
            # Create or update the ReferralProfile for the signed-up user
            referral_profile, created = ReferralProfile.objects.get_or_create(user=user)
            referral_profile.referred_by = referrer_profile.user
            referral_profile.save()
        except ReferralProfile.DoesNotExist:
            # If the referral code is invalid, do nothing
            pass

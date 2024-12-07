from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from .models import ReferralProfile, ReferralEarning


def generate_referral_link(user):
    # Assuming the user has a UserProfile with a referral_code
    return f"http://127.0.0.1:8000/accounts/signup/?ref={user.referralprofile.referral_code}"

def calculate_commission(self, payment_amount):
        """Calculate commission for a referred user's payment"""
        return (Decimal(payment_amount) * Decimal('0.001')).quantize(Decimal('0.01'))  # 0.1%

@login_required
def referral_dashboard(request):
    user = request.user
    referral_profile = ReferralProfile.objects.get(user=user)
    
    # Update total earnings
    # referral_profile.update_total_earnings()
    
    # Generate referral link
    referral_link = generate_referral_link(request.user)

    # Get referral statistics
    total_referrals = ReferralProfile.objects.filter(referred_by=request.user).count()
    
    # Get earnings for different time periods
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    
    monthly_earnings = ReferralEarning.objects.filter(
        referrer=request.user,
        created_at__gte=thirty_days_ago
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    # Get recent earnings
    recent_earnings = ReferralEarning.objects.filter(
        referrer=request.user
    ).select_related('referred_user', 'payment').order_by('-created_at')[:10]
    
    # Get referred users
    referred_users = ReferralProfile.objects.filter(
        referred_by=request.user
    ).select_related('user')
    
    context = {
        'referral_profile': referral_profile,
        'total_referrals': total_referrals,
        'monthly_earnings': monthly_earnings,
        'recent_earnings': recent_earnings,
        'referred_users': referred_users,
        'referral_link': referral_link,
    }
    return render(request, 'referrals/dashboard.html', context)

def apply_referral(request):
    """Apply referral code during registration"""
    if request.method == 'POST':
        referral_code = request.POST.get('referral_code')
        try:
            referrer_profile = ReferralProfile.objects.get(referral_code=referral_code)
            user_profile = ReferralProfile.objects.get(user=request.user)
            if not user_profile.referred_by:  # Prevent overwriting existing referral
                user_profile.referred_by = referrer_profile.user
                user_profile.save()
                messages.success(request, 'Referral code applied successfully!')
        except ReferralProfile.DoesNotExist:
            messages.error(request, 'Invalid referral code.')
    return redirect('referral_dashboard')
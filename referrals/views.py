from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import ReferralProfile, ReferralEarning

@login_required
def referral_dashboard(request):
    referral_profile = ReferralProfile.objects.get(user=request.user)
    
    # Get referral statistics
    total_referrals = ReferralProfile.objects.filter(referred_by=request.user).count()
    
    # Get earnings for different time periods
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    
    monthly_earnings = ReferralEarning.objects.filter(
        referrer=request.user,
        created_at__gte=thirty_days_ago
    ).aggregate(total=Sum('amount'))['total'] or 0
    
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
    }
    return render(request, 'referrals/dashboard.html', context)

def apply_referral(request):
    """Apply referral code during registration"""
    if request.method == 'POST':
        referral_code = request.POST.get('referral_code')
        try:
            referrer_profile = ReferralProfile.objects.get(referral_code=referral_code)
            user_profile = ReferralProfile.objects.get(user=request.user)
            user_profile.referred_by = referrer_profile.user
            user_profile.save()
            messages.success(request, 'Referral code applied successfully!')
        except ReferralProfile.DoesNotExist:
            messages.error(request, 'Invalid referral code.')
    return redirect('dashboard')
from django.shortcuts import render, redirect
from django.contrib.auth import login ,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from referrals.models import ReferralProfile
from .models import UserPreference, ActivityLog
from .utils.analytics import get_subscription_metrics, get_payment_analytics
from subscriptions.models import Subscription
from payments.models import Payment
from allauth.account.models import EmailAddress
from datetime import date
# @login_required
# def resend_verification(request):
#     if request.method == 'POST':
#         # Get the user's primary email address
#         email_address = EmailAddress.objects.filter(user=request.user, primary=True).first()
#         if email_address and not email_address.verified:
#             # Send the confirmation email
#             email_address.send_confirmation()
#             messages.success(request, "A verification email has been sent to your email address.")
#         else:
#             messages.error(request, "Email is already verified or not available.")
#         return redirect('dashboard')  # Redirect to a page after resending
#     return redirect('account_email')  # Redirect if accessed via GET

@login_required
def dashboard(request):
    # Get subscription metrics
    metrics = get_subscription_metrics(request.user)
    
    # Get active subscription
    active_subscription = Subscription.objects.filter(
        user=request.user,
        status='active'
    ).first()

    # Default to today's date if no active subscription
    active_subscription_date = active_subscription.end_date if active_subscription else date.today()
    
    # Get recent payments
    payment_history = Payment.objects.filter(
        user=request.user
    ).select_related('subscription').order_by('created_at')[:5]
    
    # Get payment analytics
    payment_analytics = get_payment_analytics(request.user)
    
    # Get recent activity
    recent_activity = ActivityLog.objects.filter(
        user=request.user
    )[:10]
    
    context = {
        'active_subscription': active_subscription,
        'active_subscription_date' : active_subscription_date,
        'payment_history': payment_history,
        'metrics': metrics,
        'payment_analytics': payment_analytics,
        'recent_activity': recent_activity,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def subscription_settings(request):
    subscriptions = Subscription.objects.filter(
        user=request.user
    ).select_related('plan')
    
    preferences, created = UserPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        preferences.email_notifications = request.POST.get('email_notifications') == 'on'
        preferences.renewal_reminders = request.POST.get('renewal_reminders') == 'on'
        preferences.newsletter_subscription = request.POST.get('newsletter_subscription') == 'on'
        preferences.save()
        
        messages.success(request, 'Preferences updated successfully!')
        return redirect('subscription_settings')
    
    context = {
        'subscriptions': subscriptions,
        'preferences': preferences,
    }
    return render(request, 'dashboard/subscription_settings.html', context)

@login_required
def activity_log(request):
    activities = ActivityLog.objects.filter(user=request.user)
    return render(request, 'dashboard/activity_log.html', {'activities': activities})

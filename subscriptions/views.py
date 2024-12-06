from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Plan , Subscription
from django.utils.timezone import now
import uuid

def plan_detail(request):
    """View to list all plans."""
    plans = Plan.objects.all()
    return render(request, 'subscriptions/plans.html', {'plans': plans})

def subscribe(request, plan_id):
    """
    View to handle subscribing to a specific plan.
    """
    plan = get_object_or_404(Plan, id=plan_id)
    
    if not request.user.is_authenticated:
        return redirect("account_login")  # Redirect to login if not authenticated    
    
    # Check if the user already has an active subscription for the selected plan
    existing_subscription = Subscription.objects.filter(user=request.user, plan=plan, is_active=True).first()
    
    if existing_subscription:
        # If there's an active subscription for this plan, show a message
        messages.info(request, 'You already have an active subscription for this plan.')
        return render(request, "subscriptions/subscribe.html", {
            "plan": plan,
        })

    # Logic to handle subscription goes here, e.g., saving user subscription
    if request.method == "POST":
        # Example: Save the subscription to the user
        # Assuming a `UserSubscription` model exists

        
        subscription = Subscription.objects.create(user=request.user)
        # Update subscription details
        subscription.plan = plan
        subscription.start_date = now()
        subscription.end_date = now() + timezone.timedelta(days=plan.duration_in_days)
        subscription.is_active = False  # Activation happens after payment
        subscription.order_id = uuid.uuid4().hex  # Generate a unique order ID
        subscription.save()         
        return redirect("payment_page",order_id=subscription.order_id) # Replace with your dashboard URL name  
    return render(request, "subscriptions/subscribe.html", {"plan": plan})


@login_required
def subscription_list(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    return render(request, "subscriptions/subscriptions.html", {"subscriptions": subscriptions})

@login_required
def cancel_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)
    if request.method == "POST":
        subscription.cancel()
        return redirect("subscription_list")
    return render(request, "subscriptions/confirm_cancel.html", {"subscription": subscription})

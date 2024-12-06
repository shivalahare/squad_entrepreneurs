import stripe
from django.conf import settings
from django.urls import reverse
from subscriptions.models import Plan, Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_checkout_session(request, plan):
    success_url = request.build_absolute_uri(
        reverse('payment_success')
    )
    cancel_url = request.build_absolute_uri(
        reverse('payment_cancel')
    )

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': plan.stripe_price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=cancel_url,
        customer_email=request.user.email,
    )
    
    return checkout_session

def handle_subscription_webhook(event):
    if event.type == 'customer.subscription.created':
        subscription = event.data.object
        handle_subscription_created(subscription)
    elif event.type == 'customer.subscription.updated':
        subscription = event.data.object
        handle_subscription_updated(subscription)
    elif event.type == 'customer.subscription.deleted':
        subscription = event.data.object
        handle_subscription_cancelled(subscription)
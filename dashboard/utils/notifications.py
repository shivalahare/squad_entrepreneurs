from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_subscription_reminder(subscription):
    """Send subscription renewal reminder"""
    context = {
        'user': subscription.user,
        'subscription': subscription,
    }
    
    message = render_to_string('dashboard/emails/renewal_reminder.html', context)
    
    send_mail(
        subject='Your Subscription is About to Renew',
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[subscription.user.email],
        html_message=message,
    )
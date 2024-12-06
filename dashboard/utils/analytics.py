from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from subscriptions.models import Subscription
from payments.models import Payment

def get_subscription_metrics(user):
    """Calculate subscription-related metrics for the user"""
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    
    return {
        'total_active': Subscription.objects.filter(
            user=user, 
            status='active'
        ).count(),
        'monthly_spend': Payment.objects.filter(
            user=user,
            created_at__gte=thirty_days_ago,
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0,
    }

# def get_payment_analytics(user):
#     """Generate payment analytics for the user"""
#     return Payment.objects.filter(
#         user=user,
#         status='completed'
#     ).values('created_at').annotate(
#         total=Sum('amount')
#     ).order_by('created_at')

def get_payment_analytics(user):
    """Generate payment analytics for the user."""
    analytics = (
        Payment.objects.filter(
            user=user,
            status='completed'
        )
        .annotate(date=TruncDate('created_at'))  # Truncate to date
        .values('date')  # Group by truncated date
        .annotate(total=Sum('amount'))  # Sum the amount for each date
        .order_by('date')
    )

    # Convert data into a format suitable for Chart.js
    dates = [entry['date'].strftime('%Y-%m-%d') for entry in analytics]
    totals = [float(entry['total']) for entry in analytics]  # Ensure amounts are numeric

    return {"dates": dates, "totals": totals}
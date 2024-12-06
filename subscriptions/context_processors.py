# subscriptions/context_processors.py

def subscription_context(request):
    return {
        "subscription_active": True,
        "subscription_plan": "Premium",
    }

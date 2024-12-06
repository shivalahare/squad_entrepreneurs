from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.plan_detail, name='plans'),
    path('subscribe/<int:plan_id>/', views.subscribe, name="subscribe"),
    path("subscriptions/", views.subscription_list, name="subscription_list"),
    path("subscriptions/cancel/<int:subscription_id>/", views.cancel_subscription, name="cancel_subscription"),
]
from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.plan_details, name='plans'),
    path('plan/<int:plan_id>/', views.plan_detail, name='plan_detail'),
    path('subscribe/<int:plan_id>/', views.subscribe, name="subscribe"),
    path("subscriptions/", views.subscription_list, name="subscription_list"),
    path("subscriptions/cancel/<int:subscription_id>/", views.cancel_subscription, name="cancel_subscription"),
    path('content/', views.educational_content, name='educational_content'),
]
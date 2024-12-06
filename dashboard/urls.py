from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('subscription_settings/', views.subscription_settings, name='subscription_settings'),
    path('activity_log/', views.activity_log, name='activity_log'),
    # path('resend-verification/', views.resend_verification, name='resend_verification'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.referral_dashboard, name='referral_dashboard'),
    path('apply/', views.apply_referral, name='apply_referral'),
]
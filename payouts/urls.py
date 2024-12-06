from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.payout_dashboard, name='payout_dashboard'),
    path('add-payment-method/', views.add_payment_method, name='add_payment_method'),
    path('request-withdrawal/', views.request_withdrawal, name='request_withdrawal'),
    path('cancel-withdrawal/<int:withdrawal_id>/', views.cancel_withdrawal, name='cancel_withdrawal'),
]
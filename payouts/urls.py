from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.payout_dashboard, name='payout_dashboard'),
    path('add-payment-method/', views.add_payment_method, name='add_payment_method'),
    path('edit-payment-method/<int:pk>/', views.edit_payment_method, name='edit_payment_method'),
    path('delete-payment-method/<int:pk>/', views.delete_payment_method, name='delete_payment_method'),
    path('payment-methods', views.payment_methods, name='payment_methods'),
    path('request-withdrawal/', views.request_withdrawal, name='request_withdrawal'),
    path('cancel-withdrawal/<int:withdrawal_id>/', views.cancel_withdrawal, name='cancel_withdrawal'),
]
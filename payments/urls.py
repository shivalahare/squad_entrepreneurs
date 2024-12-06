from django.urls import path
from . import views

urlpatterns = [
    path("payment/<str:order_id>/", views.payment_page, name="payment_page"),
]
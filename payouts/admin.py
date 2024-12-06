from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.PaymentMethod)
admin.site.register(models.WithdrawalRequest)
admin.site.register(models.WithdrawalPolicy)
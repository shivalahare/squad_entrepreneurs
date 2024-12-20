from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Plan)
admin.site.register(models.Subscription)
admin.site.register(models.Course)
admin.site.register(models.Content)
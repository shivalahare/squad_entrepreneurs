from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.UserPreference)
admin.site.register(models.ActivityLog)
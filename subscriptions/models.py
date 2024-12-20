from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.conf import settings


class Content(models.Model):
    TYPE_CHOICES = [
        ('video', 'Video'),
        ('book', 'Book'),
        ('pdf', 'PDF'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    content_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    # url = models.URLField(blank=True, null=True)  # For videos or online resources
    file = models.FileField(upload_to='uploads/', blank=True, null=True)  # For PDFs or books
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    video_thumbnail = models.FileField(upload_to='images/thumbnail/', blank=True, null=True)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=100)
    plans = models.ManyToManyField('Plan')

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

class Plan(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    duration_in_days = models.PositiveIntegerField(null=True, blank=True)
    stripe_price_id = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Subscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('pending', 'Pending'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)  # Allow NULL if needed
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    order_id = models.CharField(max_length=100, unique=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_date = models.DateField(default=datetime.date.today)
    is_active = models.BooleanField(default=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"
    
    def cancel(self):
        self.status = 'cancelled'
        self.cancelled_at = timezone.now()
        self.save()

    @property
    def is_valid(self):
        return self.status == 'active' and self.end_date > timezone.now()
    
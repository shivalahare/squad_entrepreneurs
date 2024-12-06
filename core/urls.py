from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('referrals/', include('referrals.urls')),
    path('payments/', include('payments.urls')),
    path('payouts/', include('payouts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
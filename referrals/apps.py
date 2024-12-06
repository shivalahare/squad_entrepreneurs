from django.apps import AppConfig



class ReferralsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'referrals'
    
    def ready(self):
        import referrals.signals  # Ensure signals are loaded
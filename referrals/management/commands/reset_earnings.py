from django.core.management.base import BaseCommand
from referrals.models import ReferralProfile
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Reset today\'s, weekly, and monthly earnings for all referral profiles'

    def handle(self, *args, **kwargs):
        today = datetime.today()
        for profile in ReferralProfile.objects.all():
            # Reset today's earnings
            profile.todays_earnings = 0

            # Check if it's the start of a new week (Monday)
            if today.weekday() == 0:  # Monday
                profile.weekly_earnings = 0

            # Check if it's the start of a new month
            if today.day == 1:  # First day of the month
                profile.monthly_earnings = 0

            profile.save()

        self.stdout.write(self.style.SUCCESS('Successfully reset daily, weekly, and monthly earnings'))

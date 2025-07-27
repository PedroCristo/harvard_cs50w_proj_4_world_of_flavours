from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

class Command(BaseCommand):
    """
    Creates UserProfiles for existing users who don't already have one.
    """
    help = 'Create UserProfiles for all existing users'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        users = User.objects.all()
        for user in users:
            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(user=user)
        self.stdout.write(self.style.SUCCESS('Successfully created user profiles for all users'))
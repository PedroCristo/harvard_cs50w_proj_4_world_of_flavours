from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class CustomUser(AbstractUser):
    pass

class UserProfile(models.Model):
    """
    Model for user profile info
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)
    user_image = models.ImageField(upload_to='images/profile_images/', blank=True, null=True)
    user_social_media = models.URLField(max_length=200, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username
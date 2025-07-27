# recipes/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Recipe

@receiver(post_save, sender=Recipe)
def recipe_saved(sender, instance, **kwargs):
    pass
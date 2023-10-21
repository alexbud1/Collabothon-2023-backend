# api/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Parent
import secrets

@receiver(pre_save, sender=Parent)
def generate_token(sender, instance, **kwargs):
    if not instance.token:
        instance.token = secrets.token_urlsafe(16)

# --- authz/signals.py ---
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, SecuredObjectType

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # zabezpieczenie, jeśli użytkownik istniał wcześniej bez profilu
        if not hasattr(instance, 'profile'):
            UserProfile.objects.create(user=instance)


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, SecuredObjectType
from django.db.utils import OperationalError, ProgrammingError

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            UserProfile.objects.create(user=instance)
        except (OperationalError, ProgrammingError):
            pass  # przy migracjach lub braku kolumny nie próbuj tworzyć

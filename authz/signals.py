from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.management import call_command
from .models import UserProfile
from django.db.utils import OperationalError, ProgrammingError


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            UserProfile.objects.create(user=instance)
        except (OperationalError, ProgrammingError):
            pass  # ignoruj przy migracjach lub braku kolumny


@receiver(post_migrate)
def run_init_authz(sender, **kwargs):
    if sender.name == "authz":
        try:
            call_command("init_authz_defaults")
        except Exception as e:
            print(f"[authz] init_authz_defaults failed: {e}")

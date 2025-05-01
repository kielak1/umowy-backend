# --- authz/apps.py ---
from django.apps import AppConfig

class AuthzConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authz'

    def ready(self):
        import authz.signals

        from django.contrib.auth.models import User
        from .models import SecuredObjectType, UserProfile

        # Tworzenie domyślnych SecuredObjectType jeśli nie istnieją
        defaults = [
            {"code": "contracts", "label": "Umowy"},
            {"code": "admin", "label": "Panel administracyjny"},
        ]
        for entry in defaults:
            SecuredObjectType.objects.get_or_create(code=entry["code"], defaults={"label": entry["label"]})

        # Inicjalizacja brakujących profilów dla istniejących użytkowników
        for user in User.objects.all():
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user)



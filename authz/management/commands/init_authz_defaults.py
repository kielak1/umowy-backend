from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from authz.models import UserProfile, SecuredObjectType, PermissionType 

class Command(BaseCommand):
    help = 'Tworzy domyślne wpisy SecuredObjectType i brakujące profile użytkowników'

    def handle(self, *args, **options):
        # Inicjalizacja PermissionType
        permission_map = {
            'read': {'level': 1},
            'write': {'level': 2},
            'system': {'level': 3},
            'finance': {'level': 4},
        }

        for name, data in permission_map.items():
            obj, created = PermissionType.objects.get_or_create(
                name=name, defaults={'level': data['level']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Utworzono PermissionType: {name}"))
            else:
                self.stdout.write(f"PermissionType istnieje: {name}")


        # Tworzenie wpisów contracts i admin
        for entry in [
            {"code": "contracts", "label": "Umowy"},
            {"code": "admin", "label": "Panel administracyjny"},
        ]:
            obj, created = SecuredObjectType.objects.get_or_create(code=entry["code"], defaults={"label": entry["label"]})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Utworzono: {entry['code']}"))
            else:
                self.stdout.write(f"Istnieje: {entry['code']}")

        # Tworzenie brakujących profilów
        created_count = 0
        for user in User.objects.all():
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user)
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Utworzono {created_count} brakujących profili użytkowników."))

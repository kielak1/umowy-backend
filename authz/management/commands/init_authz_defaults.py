from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from authz.models import UserProfile, SecuredObjectType, PermissionType
from umowy.models import (
    SlownikKlasyfikacjaUmowy,
    SlownikStatusUmowy,
    SlownikWlasciciel,
    SlownikObszarFunkcjonalny,
    SlownikKategoriaUmowy,
)


class Command(BaseCommand):
    help = 'Tworzy domyślne wpisy do słowników i authz (PermissionType, SecuredObjectType, UserProfile)'

    def handle(self, *args, **options):
        self.init_permissions()
        self.init_secured_objects()
        self.init_user_profiles()
        self.init_umowy_slowniki()

    def init_permissions(self):
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

    def init_secured_objects(self):
        for entry in [
            {"code": "contracts", "label": "Umowy"},
            {"code": "admin", "label": "Panel administracyjny"},
        ]:
            obj, created = SecuredObjectType.objects.get_or_create(
                code=entry["code"], defaults={"label": entry["label"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Utworzono SecuredObjectType: {entry['code']}"))
            else:
                self.stdout.write(f"SecuredObjectType istnieje: {entry['code']}")

    def init_user_profiles(self):
        created_count = 0
        for user in User.objects.all():
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user)
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Utworzono {created_count} brakujących profili użytkowników."))

    def init_umowy_slowniki(self):
        slowniki = {
            SlownikKlasyfikacjaUmowy: ["Istotna", "Nieistotna"],
            SlownikStatusUmowy: ["Obowiązująca", "Nieobowiązująca"],
            SlownikWlasciciel: ["IFS", "PKOBP S.A.", "SKOK"],
            SlownikObszarFunkcjonalny: [
                "CC_Lublin", "CSS", "CPSI/FRONT", "INNE", "LAN_DC", "L3_CORE", "TELEFONIA", "WAN"
            ],
            SlownikKategoriaUmowy: [
                "Autentykacja", "Bankomaty", "Dedykowane", "Głos", "Inne", "Internet", "Komórki",
                "LAN", "Serwis", "Sprzęt", "WAN", "Wi-Fi", "Zarządzanie"
            ],
        }

        for model, nazwy in slowniki.items():
            for nazwa in nazwy:
                obj, created = model.objects.get_or_create(nazwa=nazwa)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"[{model.__name__}] dodano: {nazwa}"))
                else:
                    self.stdout.write(f"[{model.__name__}] istnieje: {nazwa}")

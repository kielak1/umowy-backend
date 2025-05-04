# --- authz/models.py ---
from django.db import models
from django.contrib.auth.models import User

class OrganizationalUnit(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL, 
        related_name='children'
    )

    def __str__(self):
        return self.name


class PermissionType(models.Model):
    PERMISSION_CHOICES = [
        ('read', 'Read'),
        ('write', 'Write'),
        ('system', 'System'),
        ('finance', 'Finance'),
    ]

    name = models.CharField(max_length=50, choices=PERMISSION_CHOICES, unique=True)
    level = models.PositiveSmallIntegerField(help_text="Im wyższa wartość, tym szersze uprawnienie")

    class Meta:
        ordering = ['level']

    def __str__(self):
        return self.name

class SecuredObjectType(models.Model):
    code = models.CharField(max_length=100, unique=True)  # np. 'contracts', 'admin'
    label = models.CharField(max_length=255)  # np. 'Umowy', 'Panel administracyjny'

    def __str__(self):
        return self.label

class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    object_type = models.ForeignKey(SecuredObjectType, on_delete=models.CASCADE)
    org_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE)
    permission = models.ForeignKey(PermissionType, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('user', 'object_type', 'org_unit', 'permission')

    def __str__(self):
        return f"{self.user.username} / {self.object_type.code} / {self.org_unit.name} / {self.permission.name}"

class UserProfile(models.Model):
    SOURCE_CHOICES = [
        ('local', 'Lokalny'),
        ('ad', 'Active Directory'),
        ('oidc', 'OIDC'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='local')
    default_page = models.CharField(max_length=100, blank=True, null=True, help_text="Domyślna strona interfejsu użytkownika")

    def __str__(self):
        return f"Profil: {self.user.username} ({self.source})"



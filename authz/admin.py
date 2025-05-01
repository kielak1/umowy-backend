from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    OrganizationalUnit,
    PermissionType,
    SecuredObjectType,
    UserPermission,
    UserProfile,
)

@admin.register(OrganizationalUnit)
class OrganizationalUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    search_fields = ['name']
    list_filter = ['parent']

@admin.register(PermissionType)
class PermissionTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'level']
    ordering = ['level']

@admin.register(SecuredObjectType)
class SecuredObjectTypeAdmin(admin.ModelAdmin):
    list_display = ['code', 'label']
    search_fields = ['code', 'label']

@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'object_type', 'org_unit', 'permission']
    list_filter = ['object_type', 'org_unit', 'permission']
    search_fields = ['user__username']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'source']
    list_filter = ['source']
    search_fields = ['user__username']

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import OrganizationalUnit

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class OrganizationalUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationalUnit
        fields = ['id', 'name']

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
        
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        if hasattr(self.user, 'userprofile'):
            data['organizational_unit'] = self.user.userprofile.organizational_unit.name
        return data

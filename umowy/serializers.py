from rest_framework import serializers
from django.contrib.auth.models import User
from authz.models import OrganizationalUnit
from .models import Kontakt, Kontrahent, Umowa

class KontaktSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kontakt
        fields = '__all__'

class KontrahentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kontrahent
        fields = ['id', 'nazwa_kontrahenta']

class OrganizationalUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationalUnit
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UmowaSerializer(serializers.ModelSerializer):
    kontrahent = KontrahentSerializer(read_only=True)
    kontrahent_id = serializers.PrimaryKeyRelatedField(
        queryset=Kontrahent.objects.all(),
        source='kontrahent',
        write_only=True,
        required=False
    )

    opiekun = UserSerializer(read_only=True)
    opiekun_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='opiekun',
        write_only=True,
        required=False
    )

    org_unit = OrganizationalUnitSerializer(read_only=True)
    org_unit_id = serializers.PrimaryKeyRelatedField(
        queryset=OrganizationalUnit.objects.all(),
        source='org_unit',
        write_only=True,
        required=False
    )

    class Meta:
        model = Umowa
        fields = [
            'id', 'numer', 'przedmiot', 'data_zawarcia',
            'czy_wymaga_kontynuacji', 'wymagana_data_zawarcia_kolejnej_umowy',
            'czy_spelnia_wymagania_dora',
            'kontrahent', 'kontrahent_id',
            'opiekun', 'opiekun_id',
            'org_unit', 'org_unit_id',
        ]

    def update(self, instance, validated_data):
        for key in ['kontrahent', 'opiekun', 'org_unit']:
            if key in validated_data:
                setattr(instance, key, validated_data.pop(key))

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

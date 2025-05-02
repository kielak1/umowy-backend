from rest_framework import serializers
from django.contrib.auth.models import User
from authz.models import OrganizationalUnit
from .models import Kontakt, Kontrahent, Umowa, ZmianaUmowy, Zamowienie

class KontaktSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kontakt
        fields = '__all__'

class KontrahentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kontrahent
        fields = ['id', 'nazwa']


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

    jednostka_organizacyjna = OrganizationalUnitSerializer(read_only=True)
    jednostka_organizacyjna_id = serializers.PrimaryKeyRelatedField(
        queryset=OrganizationalUnit.objects.all(),
        source='jednostka_organizacyjna',
        write_only=True,
        required=False
    )

    najnowsza_zmiana = serializers.SerializerMethodField()

    class Meta:
        model = Umowa
        fields = [
            'id', 'numer',
            'czy_ramowa', 'czy_dotyczy_konkretnych_uslug',
            'czy_spelnia_dora', 'czy_wymaga_kontynuacji', 'wymagana_data_kontynuacji',
            'kontrahent', 'kontrahent_id',
            'opiekun', 'opiekun_id',
            'jednostka_organizacyjna', 'jednostka_organizacyjna_id',
            'najnowsza_zmiana',
        ]

    def get_najnowsza_zmiana(self, obj):
        zmiana = obj.zmiany.order_by('-data_zawarcia').first()
        return ZmianaUmowySerializer(zmiana).data if zmiana else None


class ZmianaUmowySerializer(serializers.ModelSerializer):
    class Meta:
        model = ZmianaUmowy
        fields = '__all__'

class ZamowienieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zamowienie
        fields = '__all__'

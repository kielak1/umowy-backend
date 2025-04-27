from rest_framework import serializers
from .models import Kontakt, Kontrahent, Umowa

class KontaktSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kontakt
        fields = '__all__'

from rest_framework import serializers
from .models import Umowa, Kontrahent

class KontrahentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kontrahent
        fields = ['id', 'nazwa_kontrahenta']

class UmowaSerializer(serializers.ModelSerializer):
    kontrahent = KontrahentSerializer(read_only=True)
    kontrahent_id = serializers.PrimaryKeyRelatedField(
        queryset=Kontrahent.objects.all(),
        source='kontrahent',
        write_only=True
    )

    class Meta:
        model = Umowa
        fields = [
            'id',
            'numer',
            'przedmiot',
            'data_zawarcia',
            'czy_wymaga_kontynuacji',
            'wymagana_data_zawarcia_kolejnej_umowy',
            'czy_spelnia_wymagania_dora',
            'kontrahent',
            'kontrahent_id',
        ]

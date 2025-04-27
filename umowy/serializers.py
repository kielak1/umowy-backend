from rest_framework import serializers
from .models import Kontakt, Kontrahent, Umowa

class KontaktSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kontakt
        fields = '__all__'

class KontrahentSerializer(serializers.ModelSerializer):
    kontakt = KontaktSerializer()

    class Meta:
        model = Kontrahent
        fields = '__all__'

class UmowaSerializer(serializers.ModelSerializer):
    kontrahent = KontrahentSerializer()

    class Meta:
        model = Umowa
        fields = '__all__'

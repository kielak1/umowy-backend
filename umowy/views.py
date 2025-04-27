from django.shortcuts import render
from rest_framework import viewsets
from .models import Kontakt, Kontrahent, Umowa
from .serializers import KontaktSerializer, KontrahentSerializer, UmowaSerializer

class KontaktViewSet(viewsets.ModelViewSet):
    queryset = Kontakt.objects.all()
    serializer_class = KontaktSerializer

class KontrahentViewSet(viewsets.ModelViewSet):
    queryset = Kontrahent.objects.all()
    serializer_class = KontrahentSerializer

class UmowaViewSet(viewsets.ModelViewSet):
    queryset = Umowa.objects.all()
    serializer_class = UmowaSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import (
    Kontakt, Kontrahent, Umowa,
    ZmianaUmowy, Zamowienie
)
from .serializers import (
    KontaktSerializer, KontrahentSerializer, UmowaSerializer,
    ZmianaUmowySerializer, ZamowienieSerializer
)


class KontaktViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Kontakt.objects.all()
    serializer_class = KontaktSerializer


class KontrahentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Kontrahent.objects.all()
    serializer_class = KontrahentSerializer


class UmowaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Umowa.objects.all()
    serializer_class = UmowaSerializer

    def get_queryset(self):
        return Umowa.objects.prefetch_related('zmiany', 'zamowienia', 'kontrahent')


class ZmianaUmowyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ZmianaUmowy.objects.all()
    serializer_class = ZmianaUmowySerializer

    def get_queryset(self):
        umowa_id = self.kwargs.get('umowa_pk') or self.request.query_params.get('umowa_id')
        if umowa_id:
            return self.queryset.filter(umowa_id=umowa_id)
        return self.queryset


class ZamowienieViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Zamowienie.objects.all()
    serializer_class = ZamowienieSerializer

    def get_queryset(self):
        # jeśli jest umowa_id w URL/query – filtrujemy tylko wtedy
        umowa_id = self.kwargs.get('umowa_pk') or self.request.query_params.get('umowa_id')
        if umowa_id:
            return self.queryset.filter(umowa_id=umowa_id)
        return self.queryset

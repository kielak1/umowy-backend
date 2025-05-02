from rest_framework import viewsets
from .models import (
    Kontakt, Kontrahent, Umowa,
    ZmianaUmowy, Zamowienie
)
from .serializers import (
    KontaktSerializer, KontrahentSerializer, UmowaSerializer,
    ZmianaUmowySerializer, ZamowienieSerializer
)


class KontaktViewSet(viewsets.ModelViewSet):
    queryset = Kontakt.objects.all()
    serializer_class = KontaktSerializer


class KontrahentViewSet(viewsets.ModelViewSet):
    queryset = Kontrahent.objects.all()
    serializer_class = KontrahentSerializer


class UmowaViewSet(viewsets.ModelViewSet):
    queryset = Umowa.objects.all()
    serializer_class = UmowaSerializer

    def get_queryset(self):
        return Umowa.objects.prefetch_related('zmiany', 'zamowienia', 'kontrahent')


class ZmianaUmowyViewSet(viewsets.ModelViewSet):
    serializer_class = ZmianaUmowySerializer

    def get_queryset(self):
        umowa_id = self.kwargs.get('umowa_pk') or self.request.query_params.get('umowa_id')
        return ZmianaUmowy.objects.filter(umowa_id=umowa_id) if umowa_id else ZmianaUmowy.objects.none()


class ZamowienieViewSet(viewsets.ModelViewSet):
    serializer_class = ZamowienieSerializer

    def get_queryset(self):
        umowa_id = self.kwargs.get('umowa_pk') or self.request.query_params.get('umowa_id')
        return Zamowienie.objects.filter(umowa_id=umowa_id) if umowa_id else Zamowienie.objects.none()

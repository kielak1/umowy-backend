from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    Kontakt, Kontrahent, Umowa, ZmianaUmowy, Zamowienie,
    SlownikKategoriaUmowy, SlownikWlasciciel, SlownikStatusUmowy,
    SlownikKlasyfikacjaUmowy, SlownikObszarFunkcjonalny,
)

from .serializers import (
    KontaktSerializer, KontrahentSerializer, UmowaSerializer,
    ZmianaUmowySerializer, ZamowienieSerializer,
    SlownikKategoriaUmowySerializer, SlownikWlascicielSerializer,
    SlownikStatusUmowySerializer, SlownikKlasyfikacjaUmowySerializer,
    SlownikObszarFunkcjonalnySerializer,
)



# === GŁÓWNE MODELE ===

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
    serializer_class = UmowaSerializer
    queryset = Umowa.objects.none()  

    def get_queryset(self):
        return (
            Umowa.objects
            .prefetch_related("zmiany", "zamowienia", "kontrahent")
            .order_by("-id")
        )


class ZmianaUmowyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ZmianaUmowySerializer
    queryset = ZmianaUmowy.objects.none()  # wymagane dla routera
    http_method_names = ['get', 'post', 'patch', 'put', 'delete']

    def get_queryset(self):
        base = ZmianaUmowy.objects.all().order_by("-id")
        if self.action == "list":
            umowa_id = self.kwargs.get('umowa_pk') or self.request.query_params.get('umowa_id')
            if umowa_id:
                return base.filter(umowa_id=umowa_id)
        return base

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if not serializer.is_valid():
            print("❌ BŁĘDNE DANE DO PATCH:", request.data)
            print("❌ BŁĘDY SERIALIZERA:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(serializer.data)
    
class ZamowienieViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ZamowienieSerializer
    queryset = Zamowienie.objects.none()  # wymagane przez router DRF

    def get_queryset(self):
        base = Zamowienie.objects.all().order_by("-id")
        umowa_id = self.kwargs.get('umowa_pk') or self.request.query_params.get('umowa_id')
        if umowa_id:
            return base.filter(umowa_id=umowa_id)
        return base

# === SŁOWNIKI ===

class SlownikKategoriaUmowyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SlownikKategoriaUmowy.objects.all()
    serializer_class = SlownikKategoriaUmowySerializer


class SlownikWlascicielViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SlownikWlasciciel.objects.all()
    serializer_class = SlownikWlascicielSerializer


class SlownikStatusUmowyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SlownikStatusUmowy.objects.all()
    serializer_class = SlownikStatusUmowySerializer


class SlownikKlasyfikacjaUmowyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SlownikKlasyfikacjaUmowy.objects.all()
    serializer_class = SlownikKlasyfikacjaUmowySerializer


class SlownikObszarFunkcjonalnyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SlownikObszarFunkcjonalny.objects.all()
    serializer_class = SlownikObszarFunkcjonalnySerializer

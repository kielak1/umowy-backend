from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from umowy.views import KontaktViewSet, KontrahentViewSet, UmowaViewSet, ZmianaUmowyViewSet, ZamowienieViewSet

from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from authz.views import UserViewSet, OrganizationalUnitViewSet

def health_check(request):
    return JsonResponse({"status": "ok"})

router = DefaultRouter()
router.register(r'kontakty', KontaktViewSet)
router.register(r'kontrahenci', KontrahentViewSet)
router.register(r'umowy', UmowaViewSet)
router.register(r'users', UserViewSet, basename='user')
router.register(r'orgunits', OrganizationalUnitViewSet, basename='orgunit')
router.register(r'zmiany', ZmianaUmowyViewSet, basename='zmianaumowy')
router.register(r'zamowienia', ZamowienieViewSet, basename='zamowienie')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('healthz/', health_check),
    path('api/auth/', include('authz.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)





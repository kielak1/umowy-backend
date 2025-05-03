from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from authz.views import (
    OrganizationalUnitViewSet,
    PermissionTypeViewSet,
    SecuredObjectTypeViewSet,
    UserPermissionViewSet,
    UserViewSet,
)
from umowy.views import (
    KontaktViewSet,
    KontrahentViewSet,
    UmowaViewSet,
    ZmianaUmowyViewSet,
    ZamowienieViewSet,
)

# Health check view
def health_check(request):
    return JsonResponse({"status": "ok"})

# Router configuration
router = DefaultRouter()
router.register(r'kontakty', KontaktViewSet)
router.register(r'kontrahenci', KontrahentViewSet)
router.register(r'umowy', UmowaViewSet)
router.register(r'zmiany', ZmianaUmowyViewSet, basename='zmianaumowy')
router.register(r'zamowienia', ZamowienieViewSet, basename='zamowienie')
router.register(r'users', UserViewSet, basename='user')
router.register(r'orgunits', OrganizationalUnitViewSet, basename='orgunit')
router.register(r'permissions/types', PermissionTypeViewSet)
router.register(r'permissions/objects', SecuredObjectTypeViewSet)
router.register(r'permissions/user', UserPermissionViewSet)

# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('authz.urls')),
    path('healthz/', health_check),
]

# Static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
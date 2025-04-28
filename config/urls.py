from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from umowy.views import KontaktViewSet, KontrahentViewSet, UmowaViewSet
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"})

router = DefaultRouter()
router.register(r'kontakty', KontaktViewSet)
router.register(r'kontrahenci', KontrahentViewSet)
router.register(r'umowy', UmowaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('healthz/', health_check),
]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

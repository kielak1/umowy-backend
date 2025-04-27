from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from umowy.views import KontaktViewSet, KontrahentViewSet, UmowaViewSet

router = DefaultRouter()
router.register(r'kontakty', KontaktViewSet)
router.register(r'kontrahenci', KontrahentViewSet)
router.register(r'umowy', UmowaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

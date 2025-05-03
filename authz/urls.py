from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    CookieTokenObtainPairView,
    CookieTokenRefreshView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Zwykłe logowanie przez body (opcjonalnie, jeśli nadal chcesz)
    path('token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair_cookie'),
    
    # Odświeżenie tokena z HttpOnly cookie
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh_cookie'),

    # (opcjonalnie) dostępne dla testów klasyczne TokenRefreshView
    path('token/refresh_raw/', TokenRefreshView.as_view(), name='token_refresh_raw'),
]

from .views import AdminUserCreateView  # dopisz do istniejących importów

urlpatterns += [
    path('admin/users/create/', AdminUserCreateView.as_view(), name='admin_user_create'),
]

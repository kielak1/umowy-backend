from django.contrib.auth.models import User
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authz.models import OrganizationalUnit
from authz.serializers import OrganizationalUnitSerializer, UserSerializer
from .models import PermissionType, SecuredObjectType, UserPermission
from .serializers import (
    AdminUserCreateSerializer,
    CustomTokenObtainPairSerializer,
    PermissionTypeSerializer,
    SecuredObjectTypeSerializer,
    UserPermissionSerializer,
    UserWithProfileSerializer,
)
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserWithProfileSerializer


class OrganizationalUnitViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = OrganizationalUnit.objects.all()
    serializer_class = OrganizationalUnitSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.get("refresh")

        if refresh:
            response.set_cookie(
                key="refresh_token",
                value=refresh,
                httponly=True,
                secure=True,
                samesite="Strict",
                path="/api/auth/token/refresh/",  # refresh działa tylko tu
            )
            del response.data["refresh"]

        return response

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"detail": "Brak refresh tokena."}, status=status.HTTP_401_UNAUTHORIZED)

        request.data["refresh"] = refresh_token
        return super().post(request, *args, **kwargs)

class PermissionTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PermissionType.objects.all()
    serializer_class = PermissionTypeSerializer

class SecuredObjectTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SecuredObjectType.objects.all()
    serializer_class = SecuredObjectTypeSerializer

class UserPermissionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer

class AdminUserCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserCreateSerializer
    queryset = User.objects.all()

from rest_framework import viewsets
from django.contrib.auth.models import User
from authz.models import OrganizationalUnit
from authz.serializers import UserSerializer, OrganizationalUnitSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OrganizationalUnitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrganizationalUnit.objects.all()
    serializer_class = OrganizationalUnitSerializer

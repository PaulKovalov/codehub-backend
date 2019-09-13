"""
CodeHub accounts view
Pavlo Kovalov 2019
"""
from rest_framework import viewsets, mixins

from accounts.models import CodehubUser
from accounts.permissions import UsersPermissions
from accounts.serializers import UserSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_class = [UsersPermissions]
    queryset = CodehubUser.objects.all()

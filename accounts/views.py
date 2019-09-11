"""
CodeHub accounts view
Pavlo Kovalov 2019
"""

from .serializers import UserSerializer
from .permissions import UsersPermissions
from django.shortcuts import render
from rest_framework import viewsets, mixins, status

class UserViewSet(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_class = [UsersPermissions]

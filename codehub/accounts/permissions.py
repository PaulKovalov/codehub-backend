from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class UsersPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj == request.user


class ViewUserPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.view_permission_all:
            return True
        else:
            if obj.view_permission_registered:
                return request.user.is_authenticated
            else:
                return False

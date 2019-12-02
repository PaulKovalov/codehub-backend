from rest_framework import permissions


class UsersPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return request.user == obj


class ViewUserPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.view_permission_all:
            return True
        else:
            if obj.view_permission_registered:
                return request.user.is_authenticated
            else:
                return False

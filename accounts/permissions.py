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
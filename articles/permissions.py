from rest_framework import permissions


class ArticlePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET' or request.method == 'OPTIONS':
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return obj in request.user.articless

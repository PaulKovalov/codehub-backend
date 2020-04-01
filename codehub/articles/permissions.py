from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class ArticlePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser or (request.user.is_authenticated and obj in request.user.articles.all())

from rest_framework import permissions

class ArticlePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        print(request.method)
        if request.method == 'GET':
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print(request.method)
        if not request.user.is_authenticated:
            return False
        if obj in request.user.articles:
            return True

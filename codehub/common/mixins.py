from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response


class MyContentListMixin:
    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def my(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class RecentContentListMixin:
    @action(methods=['GET'], detail=False, permission_classes=[AllowAny])
    def recent(self, request, *args, **kwargs):
        qs = self.get_queryset().order_by('date_created')[:5]
        return Response(self.get_serializer(qs, many=True).data)

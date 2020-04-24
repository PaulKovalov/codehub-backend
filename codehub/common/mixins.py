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


class CustomRetrieveMixin:
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if instance.published:
            views = instance.views
            instance.views = views + 1
            instance.save()
        return Response(serializer.data)


class ReactModelMixin:
    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, *args, **kwargs):
        lookup_kwarg = self.get_reaction_lookup_kwargs()
        reaction_model = self.get_reaction_model()
        if reaction_model.objects.filter(**lookup_kwarg, user=self.request.user, type='like'):
            reaction_model.objects.get(**lookup_kwarg, user=self.request.user, type='like').delete()
            return Response(data='dec')
        else:
            obj, created = reaction_model.objects.update_or_create(**lookup_kwarg, user=self.request.user,
                                                                   defaults={'type': 'like'})
            if created:
                return Response(data='inc')
            else:
                return Response(data='swap')

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def dislike(self, request, *args, **kwargs):
        lookup_kwarg = self.get_reaction_lookup_kwargs()
        reaction_model = self.get_reaction_model()
        if reaction_model.objects.filter(**lookup_kwarg, user=self.request.user, type='dislike'):
            reaction_model.objects.get(**lookup_kwarg, user=self.request.user, type='dislike').delete()
            return Response(data='dec')
        obj, created = reaction_model.objects.update_or_create(**lookup_kwarg, user=self.request.user,
                                                               defaults={'type': 'dislike'})
        if created:
            return Response(data='inc')
        else:
            return Response(data='swap')

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from articles.tools import get_preview, get_reading_time
from articles.utils import DefaultPaginator
from common.mixins import MyContentListModelMixin
from tutorials.models import Tutorial, TutorialArticle
from tutorials.paginators import TutorialArticlesPaginator
from tutorials.permissions import TutorialPermission, TutorialArticlePermission
from tutorials.serializers import TutorialSerializer, TutorialArticleSerializer, TutorialArticlePreviewSerializer, \
    MyTutorialArticlePreviewSerializer, MyTutorialSerializer


class TutorialsViewSet(viewsets.ModelViewSet, MyContentListModelMixin):
    permission_classes = [TutorialPermission]
    serializer_class = TutorialSerializer
    pagination_class = DefaultPaginator

    def get_queryset(self):
        qs = Tutorial.objects.filter(published=True)
        if self.request.user.is_authenticated:
            if self.action == 'my' or self.action == 'my_count' or self.action == 'partial_update':
                qs = Tutorial.objects.filter(author=self.request.user)
            if self.action == 'retrieve':
                qs = qs | Tutorial.objects.filter(author=self.request.user)
        return qs.distinct()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.action == 'my':
                return MyTutorialSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated], url_name='my-tutorials-count',
            url_path='my/count')
    def my_count(self, requset, *args, **kwargs):
        count = self.get_queryset().count()
        return Response(data={'count': count})

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated], url_name='my-tutorials-ids',
            url_path='my/ids')
    def my_ids(self, request, *args, **kwargs):
        ids = Tutorial.objects.filter(author=self.request.user).values_list('id', flat=True)
        return Response(data=ids)


class TutorialArticlesViewSet(viewsets.ModelViewSet, MyContentListModelMixin):
    permission_classes = [TutorialArticlePermission]
    serializer_class = TutorialArticleSerializer
    pagination_class = TutorialArticlesPaginator

    def get_queryset(self):
        tutorial_pk = self.kwargs['tutorial_pk']
        tutorial = get_object_or_404(Tutorial, id=tutorial_pk)
        qs = TutorialArticle.objects.filter(tutorial__pk=tutorial_pk, published=True)
        user = self.request.user
        if user.is_authenticated and tutorial.author == user:
            qs = TutorialArticle.objects.filter(tutorial__pk=tutorial_pk)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return TutorialArticlePreviewSerializer
        if self.action == 'my':
            return MyTutorialArticlePreviewSerializer
        return super().get_serializer_class()

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context()
        context.update({'tutorial': Tutorial.objects.get(id=self.kwargs['tutorial_pk'])})
        return context

    def perform_create(self, serializer):
        tutorial = get_object_or_404(Tutorial, id=self.kwargs['tutorial_pk'])
        text = serializer.validated_data['text']
        last_article_order = -1
        if tutorial.articles.all().count():
            last_article_order = tutorial.articles.order_by('order').last().order
        serializer.save(author=self.request.user, tutorial=tutorial, preview=get_preview(text),
                        estimate_reading_time=get_reading_time(text), order=last_article_order + 1)

    @action(methods=['GET'], detail=False, permission_classes=[AllowAny], url_path='table-of-content')
    def table_of_content(self, request, *args, **kwargs):
        qs = self.get_queryset()
        toc = [{'title': a.title, 'id': a.id} for a in qs.order_by('order')]
        return Response(data=toc)
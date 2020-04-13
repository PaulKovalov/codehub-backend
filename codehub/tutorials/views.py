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
from tutorials.permissions import TutorialPermission, TutorialArticlePermission
from tutorials.serializers import TutorialSerializer, TutorialArticleSerializer, TutorialArticlePreviewSerializer, \
    MyTutorialArticlePreviewSerializer


class TutorialsViewSet(viewsets.ModelViewSet, MyContentListModelMixin):
    permission_classes = [TutorialPermission]
    serializer_class = TutorialSerializer
    pagination_class = DefaultPaginator

    def get_queryset(self):
        qs = Tutorial.objects.filter(published=True)
        if self.request.user.is_authenticated and (self.action == 'my' or self.action == 'my_count'):
            qs = Tutorial.objects.filter(author=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated], url_name='my-tutorials-count',
            url_path='my/count')
    def my_count(self, requset, *args, **kwargs):
        count = self.get_queryset().count()
        return Response(data={'count': count})


class TutorialArticlesViewSet(viewsets.ModelViewSet, MyContentListModelMixin):
    permission_classes = [TutorialArticlePermission]
    serializer_class = TutorialArticleSerializer
    pagination_class = DefaultPaginator

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

    def perform_create(self, serializer):
        tutorial = get_object_or_404(Tutorial, id=self.kwargs['tutorial_pk'])
        text = serializer.validated_data['text']
        serializer.save(author=self.request.user, tutorial=tutorial, preview=get_preview(text),
                        estimate_reading_time=get_reading_time(text))

    @action(methods=['GET'], detail=False, permission_classes=[AllowAny])
    def table_of_content(self, request, *args, **kwargs):
        qs = self.get_queryset()
        toc = [{'title': a.title, 'id': a.id} for a in qs]
        return Response(data=toc)

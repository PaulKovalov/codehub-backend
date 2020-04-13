"""
Codehub Article API endpoints
Pavlo Kovalov 2019
"""
import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from articles.models import Article
from articles.permissions import ArticlePermission
from articles.serializers import ArticleSerializer, ArticlePreviewSerializer, MyArticlesPreviewSerializer
from articles.tools import get_preview, get_reading_time
from articles.utils import DefaultPaginator
from common.mixins import MyContentListModelMixin


class ArticlesViewSet(viewsets.ModelViewSet, MyContentListModelMixin):
    permission_classes = [ArticlePermission]
    serializer_class = ArticleSerializer
    pagination_class = DefaultPaginator

    def get_queryset(self):
        qs = Article.objects.filter(published=True)
        if self.request.user.is_authenticated:
            if self.action == 'my' or self.action == 'partial_update':
                return Article.objects.filter(author=self.request.user)
        return qs

    def perform_create(self, serializer):
        text = serializer.validated_data['text']
        serializer.save(author=self.request.user, preview=get_preview(text),
                        estimate_reading_time=get_reading_time(text))

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return ArticlePreviewSerializer
        if self.action == 'my':
            return MyArticlesPreviewSerializer
        return super().get_serializer_class()

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated], url_name='my-articles-count',
            url_path='my/count')
    def my_count(self, requset, *args, **kwargs):
        count = Article.objects.filter(author=self.request.user).count()
        return Response(data={'count': count})

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated], url_name='my-articles-ids',
            url_path='my/ids')
    def my_ids(self, request, *args, **kwargs):
        ids = Article.objects.filter(author=self.request.user).values_list('id', flat=True)
        return Response(data=ids)

    @action(methods=['GET'], detail=False)
    def recent(self, request, *args, **kwargs):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        qs = self.get_queryset()
        qs = qs.filter(date_created__gt=yesterday).order_by('views')[:5]
        return Response(ArticlePreviewSerializer(qs, many=True).data)

"""
Codehub Article API endpoints
Pavlo Kovalov 2019
"""

from rest_framework import viewsets

from articles.models import Article
from articles.permissions import ArticlePermission
from articles.serializers import ArticleSerializer
from articles.utils import ArticlePaginator


class ArticlesViewSet(viewsets.ModelViewSet):
    permission_classes = [ArticlePermission]
    serializer_class = ArticleSerializer
    pagination_class = ArticlePaginator
    queryset = Article.objects

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
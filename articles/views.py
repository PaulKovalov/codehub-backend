"""
Codehub Article API endpoints
Pavlo Kovalov 2019
"""
import logging

from rest_framework import viewsets

from articles.models import Article
from articles.permissions import ArticlePermission
from articles.serializers import ArticleSerializer

logger = logging.getLogger(__name__)


class ArticlesViewSet(viewsets.ModelViewSet):
    permission_classes = [ArticlePermission]
    serializer_class = ArticleSerializer

    def get_queryset(self):
        starting_from = self.request.data.get('from', 0)
        data = Article.objects.filter(published=True).order_by('-id')[starting_from: 10 + starting_from]
        return data

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

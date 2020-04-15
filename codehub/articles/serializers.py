"""
Codehub Article Serializer
Pavlo Kovalov 2019
"""

from rest_framework import serializers

from articles.models import Article
from common.base_article_serializer import BaseArticleSerializer


class ArticleSerializer(BaseArticleSerializer):
    class Meta:
        model = Article
        read_only_fields = ('date_created', 'views', 'id', 'estimate_reading_time', 'author', 'username',
                            'last_modified')
        fields = ('title', 'text', 'published') + read_only_fields


class ArticlePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        read_only_fields = (
            'id', 'date_created', 'views', 'estimate_reading_time', 'author', 'title', 'preview', 'username')
        fields = read_only_fields


class MyArticlesPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        read_only_fields = (
            'id', 'date_created', 'views', 'estimate_reading_time', 'author', 'title', 'preview', 'published',
            'username')
        fields = read_only_fields

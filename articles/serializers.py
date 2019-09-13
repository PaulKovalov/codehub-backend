"""
Codehub Article Serializer
Pavlo Kovalov 2019
"""

from rest_framework import serializers

from articles.article_processor import ArticleProcessor
from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'views', 'date_created', 'text']

    def validate_title(self, value):
        article_processor = ArticleProcessor()
        article_processor.validate_title(value)
        return value

    def validate_text(self, value):
        article_processor = ArticleProcessor()
        article_processor.validate_text(value)
        return value

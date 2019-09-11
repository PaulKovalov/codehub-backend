"""
Codehub Article Serializer
Pavlo Kovalov 2019
"""

from rest_framework import serializers
from .article_processor import ArticleProcessor
from articles.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id','title','views','date_created','text']

    def validate_title(self, value):
        articleProcessor = ArticleProcessor()
        articleProcessor.validate_title(value)
        return value

    def validate_text(self, value):
        articleProcessor = ArticleProcessor()
        articleProcessor.validate_text(value)
        return value
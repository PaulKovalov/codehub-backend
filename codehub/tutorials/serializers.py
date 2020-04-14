from rest_framework import serializers

from common.base_article_serializer import BaseArticleSerializer
from tutorials.models import Tutorial, TutorialArticle


class TutorialArticleSerializer(BaseArticleSerializer):
    class Meta:
        model = TutorialArticle
        read_only_fields = ('date_created', 'views', 'id', 'estimate_reading_time', 'author', 'username', 'tutorial')
        fields = ('title', 'text', 'published') + read_only_fields


class TutorialArticlePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialArticle
        read_only_fields = (
            'id', 'date_created', 'views', 'estimate_reading_time', 'author', 'title', 'preview', 'username',
            'tutorial')
        fields = read_only_fields


class TutorialSerializer(serializers.ModelSerializer):
    articles = TutorialArticlePreviewSerializer(many=True, read_only=True)

    class Meta:
        model = Tutorial
        read_only_fields = ('id', 'views', 'author', 'username', 'total_views', 'date_created', 'articles',
                            'total_articles')
        fields = ('title', 'preview') + read_only_fields


class MyTutorialSerializer(serializers.ModelSerializer):
    articles = TutorialArticlePreviewSerializer(many=True, read_only=True)

    class Meta:
        model = Tutorial
        read_only_fields = ('id', 'views', 'author', 'username', 'total_views', 'date_created', 'articles',
                            'total_articles', 'published')
        fields = ('title', 'preview') + read_only_fields


class MyTutorialArticlePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialArticle
        read_only_fields = (
            'id', 'date_created', 'views', 'estimate_reading_time', 'author', 'title', 'preview', 'published',
            'username',)
        fields = read_only_fields

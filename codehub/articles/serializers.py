"""
Codehub Article Serializer
Pavlo Kovalov 2019
"""

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        read_only_fields = ('date_created', 'views', 'id', 'estimate_reading_time', 'author', 'username')
        fields = ('title', 'text', 'published') + read_only_fields

    def validate_title(self, value):
        if len(value) >= settings.ARTICLE_TITLE_MAX_LENGTH:
            raise serializers.ValidationError('Title is too long')
        if len(value) < settings.ARTICLE_TITLE_MIN_LENGTH:
            raise serializers.ValidationError('Title is too short')
        return value

    def validate_text(self, value):
        if len(value) >= settings.ARTICLE_CONTENT_MAX_LENGTH:
            raise serializers.ValidationError('Text is too long')
        if len(value) < settings.ARTICLE_CONTENT_MIN_LENGTH:
            raise serializers.ValidationError('Text is too short')
        return value

    def update(self, instance, validated_data):
        published = validated_data.get('published')
        new_text = validated_data.get('text')
        new_title = validated_data.get('title')
        if published is not None:
            user = self.context.get('request').user
            if user.is_superuser:
                instance.published = published
            else:
                raise PermissionDenied('This field can be edited only by superuser')
        if new_text:
            instance.text = new_text
        if new_title:
            instance.title = new_title
        instance.published = False
        instance.save()
        return instance


class ListArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        read_only_fields = (
            'id', 'date_created', 'views', 'estimate_reading_time', 'author', 'title', 'preview', 'username')
        fields = read_only_fields


class MyArticlesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        read_only_fields = (
            'id', 'date_created', 'views', 'estimate_reading_time', 'author', 'title', 'preview', 'published',
            'username')
        fields = read_only_fields

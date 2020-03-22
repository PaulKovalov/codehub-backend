"""
Codehub Article Serializer
Pavlo Kovalov 2019
"""

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        read_only_fields = ('date_created', 'views', 'id', 'estimate_reading_time', 'author')
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
        if published is not None:
            user = self.context.get('request').user
            if user.is_superuser:
                instance.published = published
            else:
                raise ValidationError('This field can be edited only by superuser')
        instance.save()
        return instance

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from articles.models import Article, ArticleComment
from common.serializers import BaseArticleSerializer


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


class ArticleCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ArticleComment
        read_only_fields = ('id', 'article', 'author', 'username', 'date_created',
                            'replies', 'likes', 'dislikes', 'edited')
        fields = read_only_fields + ('text', 'reply_to')

    def get_replies(self, instance):
        qs = instance.article.comments.filter(reply_to=instance)
        return [c.id for c in qs]

    def validate_text(self, text):
        if text:
            if len(text) > settings.COMMENT_MAX_LENGTH:
                raise ValidationError('\'text\' is too long!')
            if len(text) == 0:
                raise ValidationError('\'text\' is empty')
        else:
            raise ValidationError('\'text\' is None')
        return text

from rest_framework import serializers

from articles.models import Article, ArticleComment
from common.serializers import BaseArticleSerializer, BaseCommentSerializer


class ArticleSerializer(BaseArticleSerializer):
    dislikes = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        read_only_fields = ('date_created', 'views', 'id', 'estimate_reading_time', 'author', 'username',
                            'last_modified', 'likes', 'dislikes')
        fields = ('title', 'text', 'published') + read_only_fields

    def get_likes(self, instance):
        return instance.reactions.all().filter(type='like').count()

    def get_dislikes(self, instance):
        return instance.reactions.all().filter(type='dislike').count()


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


class ArticleCommentSerializer(BaseCommentSerializer):
    class Meta:
        model = ArticleComment
        read_only_fields = ('id', 'article', 'author', 'username', 'date_created',
                            'replies', 'likes', 'dislikes', 'edited')
        fields = read_only_fields + ('text', 'reply_to')

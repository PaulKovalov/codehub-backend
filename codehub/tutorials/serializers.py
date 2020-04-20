from django.utils import timezone
from rest_framework import serializers

from common.serializers import BaseArticleSerializer, BaseCommentSerializer
from tutorials.models import Tutorial, TutorialArticle, TutorialArticleComment


class TutorialArticleSerializer(BaseArticleSerializer):
    nav = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TutorialArticle
        read_only_fields = ('date_created', 'views', 'id', 'estimate_reading_time', 'author', 'username', 'tutorial')
        fields = ('title', 'text', 'published', 'nav', 'last_modified') + read_only_fields

    def get_nav(self, instance):
        tutorial = instance.tutorial
        qs = tutorial.articles.all()
        if self.context.get('request').user.is_authenticated and tutorial.author == self.context.get('request').user:
            next_article = qs.filter(order__gt=instance.order).first()
            prev_article = qs.filter(order__lt=instance.order).last()
        else:
            next_article = qs.filter(published=True, order__gt=instance.order).first()
            prev_article = qs.filter(published=True, order__lt=instance.order).last()
        next_article_id = next_article.id if next_article else -1
        prev_article_id = prev_article.id if prev_article else -1
        return {'next': next_article_id, 'prev': prev_article_id}


class TutorialArticlePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialArticle
        read_only_fields = (
            'id', 'date_created', 'views', 'estimate_reading_time', 'author', 'title', 'preview', 'username',
            'tutorial')
        fields = read_only_fields


class MyTutorialArticlePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialArticle
        read_only_fields = (
            'id', 'date_created', 'views', 'estimate_reading_time', 'author', 'title', 'preview', 'published',
            'username', 'order')
        fields = read_only_fields


class TutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        read_only_fields = ('id', 'views', 'author', 'username', 'total_views', 'date_created',
                            'total_articles', 'last_modified')
        fields = ('title', 'preview') + read_only_fields

    def update(self, instance, validated_data):
        if validated_data.get('title') or validated_data.get('preview'):
            instance.last_modified = timezone.now()
        return super().update(instance, validated_data)


class MyTutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        read_only_fields = ('id', 'views', 'author', 'username', 'total_views', 'date_created',
                            'total_articles', 'published', 'last_modified')
        fields = ('title', 'preview') + read_only_fields


class TutorialArticleCommentSerializer(BaseCommentSerializer):
    class Meta:
        model = TutorialArticleComment
        read_only_fields = ('id', 'article', 'author', 'username', 'date_created',
                            'replies', 'likes', 'dislikes', 'edited')
        fields = read_only_fields + ('text', 'reply_to')

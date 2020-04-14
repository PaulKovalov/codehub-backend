from rest_framework import serializers

from common.base_article_serializer import BaseArticleSerializer
from tutorials.models import Tutorial, TutorialArticle


class TutorialArticleSerializer(BaseArticleSerializer):
    nav = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TutorialArticle
        read_only_fields = ('date_created', 'views', 'id', 'estimate_reading_time', 'author', 'username', 'tutorial')
        fields = ('title', 'text', 'published', 'nav') + read_only_fields

    def get_nav(self, instance):
        tutorial = self.context.get('tutorial')
        qs = tutorial.articles.order_by('order')
        if self.context.get('request').user.is_authenticated:
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
                            'total_articles')
        fields = ('title', 'preview') + read_only_fields


class MyTutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        read_only_fields = ('id', 'views', 'author', 'username', 'total_views', 'date_created',
                            'total_articles', 'published')
        fields = ('title', 'preview') + read_only_fields

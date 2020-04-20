from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from tutorials.models import TutorialArticle


class BaseArticleSerializer(serializers.ModelSerializer):

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
            instance.last_modified = timezone.now()
            if isinstance(instance, TutorialArticle):
                instance.tutorial.last_modified = timezone.now()
                instance.tutorial.save()
        if new_title:
            instance.title = new_title
            instance.last_modified = timezone.now()
            if isinstance(instance, TutorialArticle):
                instance.tutorial.last_modified = timezone.now()
                instance.tutorial.save()
        instance.published = False
        instance.save()
        return instance


class BaseCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    dislikes = serializers.SerializerMethodField(read_only=True)

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

    def get_likes(self, instance):
        return instance.reactions.all().filter(type='like').count()

    def get_dislikes(self, instance):
        return instance.reactions.all().filter(type='dislike').count()

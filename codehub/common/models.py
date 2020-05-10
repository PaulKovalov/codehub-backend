from django.conf import settings
from django.db import models

from accounts.models import User


class ReactionBaseModel(models.Model):
    TYPES = (
        ('like', 'like'),
        ('dislike', 'dislike'),
    )
    type = models.CharField(choices=TYPES, max_length=8)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class CommentBaseModel(models.Model):
    article = None
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    edited = models.BooleanField(default=False)

    @property
    def username(self):
        if self.author:
            return self.author.username

    class Meta:
        abstract = True


class ArticleBaseModel(models.Model):
    title = models.CharField(max_length=settings.ARTICLE_TITLE_MAX_LENGTH)
    views = models.IntegerField(default=0)
    date_created = models.DateTimeField('Date created', auto_now_add=True)
    published = models.BooleanField(default=False)
    text = models.TextField(default='article content', max_length=settings.ARTICLE_CONTENT_MAX_LENGTH)
    estimate_reading_time = models.IntegerField(default=1)
    preview = models.TextField()
    last_modified = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def username(self):
        return self.author.username

    class Meta:
        abstract = True

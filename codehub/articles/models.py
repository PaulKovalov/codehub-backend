from django.conf import settings
from django.db import models

from accounts.models import User


class Article(models.Model):
    title = models.CharField(max_length=settings.ARTICLE_TITLE_MAX_LENGTH)
    views = models.IntegerField(default=0)
    author = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
    date_created = models.DateTimeField('Date created', auto_now_add=True)
    published = models.BooleanField(default=False)
    text = models.TextField(default='article content', max_length=settings.ARTICLE_CONTENT_MAX_LENGTH, db_index=True)
    estimate_reading_time = models.IntegerField(default=1)
    preview = models.TextField()
    last_modified = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def username(self):
        return self.author.username


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='article_comments')
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    reply_to = models.ForeignKey('articles.ArticleComment', null=True, on_delete=models.CASCADE, related_name='replies')
    edited = models.BooleanField(default=False)

    @property
    def username(self):
        if self.author:
            return self.author.username

"""
Codehub Article app models
Pavlo Kovalov 2019
"""
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

    def __str__(self):
        return self.title

    @property
    def username(self):
        return self.author.username

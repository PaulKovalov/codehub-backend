"""
Codehub Article app models
Pavlo Kovalov 2019
"""
from accounts.models import CodehubUser
from django.db import models
from codehub import config

class Article(models.Model):
    title = models.CharField(max_length=config.ARTICLE_TITLE_MAX_LENGTH)
    views = models.IntegerField(default=0)
    author = models.ForeignKey(CodehubUser, related_name='articles', on_delete=models.CASCADE)
    date_created = models.DateTimeField('Date created', auto_now_add=True)
    published = models.BooleanField(default=False)
    text = models.TextField(default='article content', max_length=config.ARTICLE_CONTENT_MAX_LENGTH, db_index=True)
    estimate_reading_time = models.IntegerField(default=1)

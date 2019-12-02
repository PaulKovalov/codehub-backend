from django.db import models

from accounts.models import CodehubUser
from articles.models import Article
from codehub import config


class Tutorial(models.Model):
    title = models.CharField(max_length=config.TUTORIAL_TITLE_MAX_LENGTH, blank=False)
    views = models.IntegerField(default=0)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(CodehubUser, on_delete=models.CASCADE)
    articles = models.ForeignKey(Article, null=True, on_delete=models.CASCADE)

from django.conf import settings
from django.db import models

from accounts.models import User
from articles.models import Article


class Tutorial(models.Model):
    title = models.CharField(max_length=settings.TUTORIAL_TITLE_MAX_LENGTH, blank=False)
    views = models.IntegerField(default=0)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    articles = models.ForeignKey(Article, null=True, on_delete=models.CASCADE)

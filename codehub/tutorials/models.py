from django.conf import settings
from django.db import models

from accounts.models import User


class TutorialArticle(models.Model):
    title = models.CharField(max_length=settings.ARTICLE_TITLE_MAX_LENGTH)
    views = models.IntegerField(default=0)
    date_created = models.DateTimeField('Date created', auto_now_add=True)
    published = models.BooleanField(default=False)
    text = models.TextField(default='article content', max_length=settings.ARTICLE_CONTENT_MAX_LENGTH, db_index=True)
    estimate_reading_time = models.IntegerField(default=1)
    preview = models.TextField()
    tutorial = models.ForeignKey('tutorials.Tutorial', on_delete=models.CASCADE, related_name='articles')
    author = models.ForeignKey(User, related_name='tutorial_articles', on_delete=models.CASCADE)

    @property
    def username(self):
        return self.author.username


class Tutorial(models.Model):
    title = models.CharField(max_length=settings.TUTORIAL_TITLE_MAX_LENGTH, blank=False)
    views = models.IntegerField(default=0)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutorials')
    date_created = models.DateTimeField(auto_now_add=True)
    preview = models.TextField(max_length=settings.TUTORIAL_PREVIEW_MAX_LENGTH, blank=True, null=True)

    @property
    def total_views(self):
        count = 0
        for article in self.articles.all():
            count += article.views
        return count

    @property
    def username(self):
        return self.author.username

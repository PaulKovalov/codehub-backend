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
    tutorial = models.ForeignKey('tutorials.Tutorial', on_delete=models.CASCADE, related_name='articles', null=True)
    author = models.ForeignKey(User, related_name='tutorial_articles', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    last_modified = models.DateTimeField(blank=True, null=True)

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
    last_modified = models.DateTimeField(blank=True, null=True)

    @property
    def total_views(self):
        count = 0
        for article in self.articles.all():
            count += article.views
        return count

    @property
    def total_articles(self):
        return self.articles.all().count()

    @property
    def username(self):
        return self.author.username


class TutorialArticleComment(models.Model):
    article = models.ForeignKey(TutorialArticle, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='tutorial_articles_comments')
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    reply_to = models.ForeignKey('tutorials.TutorialArticleComment', null=True, on_delete=models.CASCADE,
                                 related_name='replies')
    edited = models.BooleanField(default=False)

    @property
    def username(self):
        if self.author:
            return self.author.username


class TutorialArticleCommentReaction(models.Model):
    TYPES = (
        ('like', 'like'),
        ('dislike', 'dislike'),
    )

    comment = models.ForeignKey(TutorialArticleComment, on_delete=models.CASCADE, related_name='reactions')
    type = models.CharField(choices=TYPES, max_length=8)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['comment', 'user'], name='user_tutorial_article_comment')
        ]


class TutorialArticleReaction(models.Model):
    TYPES = (
        ('like', 'like'),
        ('dislike', 'dislike'),
    )

    article = models.ForeignKey(TutorialArticle, on_delete=models.CASCADE, related_name='reactions')
    type = models.CharField(choices=TYPES, max_length=8)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['article', 'user'], name='user_tutorial_article')
        ]

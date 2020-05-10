from django.conf import settings
from django.db import models

from accounts.models import User
from common.models import ReactionBaseModel, CommentBaseModel, ArticleBaseModel


class TutorialArticle(ArticleBaseModel):
    tutorial = models.ForeignKey('tutorials.Tutorial', on_delete=models.CASCADE, related_name='articles', null=True)
    author = models.ForeignKey(User, related_name='tutorial_articles', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    @property
    def location(self):
        return f'/tutorials/{self.tutorial.id}/articles/{self.id}'


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

    @property
    def location(self):
        return f'/tutorials/{self.id}'


class TutorialArticleComment(CommentBaseModel):
    article = models.ForeignKey(TutorialArticle, on_delete=models.CASCADE, related_name='comments')
    reply_to = models.ForeignKey('tutorials.TutorialArticleComment', null=True, on_delete=models.CASCADE,
                                 related_name='replies')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='tutorial_articles_comments')


class TutorialArticleCommentReaction(ReactionBaseModel):
    comment = models.ForeignKey(TutorialArticleComment, on_delete=models.CASCADE, related_name='reactions')

    class Meta(ReactionBaseModel.Meta):
        constraints = [
            models.UniqueConstraint(fields=['comment', 'user'], name='user_tutorial_article_comment')
        ]


class TutorialArticleReaction(ReactionBaseModel):
    article = models.ForeignKey(TutorialArticle, on_delete=models.CASCADE, related_name='reactions')

    class Meta(ReactionBaseModel.Meta):
        constraints = [
            models.UniqueConstraint(fields=['article', 'user'], name='user_tutorial_article')
        ]

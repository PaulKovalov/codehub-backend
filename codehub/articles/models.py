from django.db import models

from accounts.models import User
from common.models import ReactionBaseModel, CommentBaseModel, ArticleBaseModel


class Article(ArticleBaseModel):
    author = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)


class ArticleComment(CommentBaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='article_comments')
    reply_to = models.ForeignKey('articles.ArticleComment', null=True, on_delete=models.CASCADE, related_name='replies')


class CommentReaction(ReactionBaseModel):
    comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, related_name='reactions')

    class Meta(ReactionBaseModel.Meta):
        constraints = [
            models.UniqueConstraint(fields=['comment', 'user'], name='user_comment')
        ]


class ArticleReaction(ReactionBaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reactions')

    class Meta(ReactionBaseModel.Meta):
        constraints = [
            models.UniqueConstraint(fields=['article', 'user'], name='user_article')
        ]

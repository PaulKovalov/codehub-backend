from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from articles.models import Article, CommentReaction, ArticleReaction
from articles.permissions import ArticlePermission
from articles.serializers import ArticleSerializer, ArticlePreviewSerializer, MyArticlesPreviewSerializer, \
    ArticleCommentSerializer
from articles.tools import get_preview, get_reading_time
from articles.utils import DefaultPaginator
from codehub.tasks import send_mail_on_new_comment
from common.mixins import MyContentListMixin, RecentContentListMixin, CustomRetrieveMixin, ReactModelMixin


class ArticlesViewSet(mixins.CreateModelMixin, CustomRetrieveMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet, MyContentListMixin, RecentContentListMixin,
                      ReactModelMixin):
    permission_classes = [ArticlePermission]
    serializer_class = ArticleSerializer
    pagination_class = DefaultPaginator

    def get_queryset(self):
        qs = Article.objects.filter(published=True)
        if self.request.user.is_authenticated:
            if self.action == 'my' or self.action == 'partial_update':
                return Article.objects.filter(author=self.request.user)
            if self.action == 'retrieve':
                qs = qs | Article.objects.filter(author=self.request.user)
        return qs

    def get_reaction_model(self):
        return ArticleReaction

    def get_reaction_lookup_kwargs(self):
        return dict(article=self.get_object())

    def perform_create(self, serializer):
        text = serializer.validated_data['text']
        serializer.save(author=self.request.user, preview=get_preview(text),
                        estimate_reading_time=get_reading_time(text))

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list' or self.action == 'recent':
            return ArticlePreviewSerializer
        if self.action == 'my':
            return MyArticlesPreviewSerializer
        return super().get_serializer_class()

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated], url_name='my-articles-count',
            url_path='my/count')
    def my_count(self, requset, *args, **kwargs):
        count = Article.objects.filter(author=self.request.user).count()
        return Response(data={'count': count})

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated], url_name='my-articles-ids',
            url_path='my/ids')
    def my_ids(self, request, *args, **kwargs):
        ids = Article.objects.filter(author=self.request.user).values_list('id', flat=True)
        return Response(data=ids)


class ArticleCommentsViewSet(viewsets.ModelViewSet, ReactModelMixin):
    serializer_class = ArticleCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPaginator

    def get_reaction_model(self):
        return CommentReaction

    def get_reaction_lookup_kwargs(self):
        return dict(comment=self.get_object())

    def perform_create(self, serializer):
        author = self.request.user
        article = get_object_or_404(Article, id=self.kwargs['article_pk'], published=True)
        comment = serializer.save(author=author, article=article)
        send_mail_on_new_comment.delay(article.author.email, author.username, article.location, comment.text,
                                       article.title)

    def get_queryset(self):
        article = get_object_or_404(Article, id=self.kwargs['article_pk'], published=True)
        return article.comments.all()

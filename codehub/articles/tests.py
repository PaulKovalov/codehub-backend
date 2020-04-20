from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from articles.models import Article, ArticleComment, CommentReaction
from articles.serializers import ArticlePreviewSerializer, ArticleCommentSerializer


class TestArticleCreate(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = mommy.make(User)

    def test_create_article(self):
        data = {
            'title': 'Random article title',
            'text': 'random article text' * 5
        }
        url = reverse('articles-list')
        self.client.force_authenticate(self.author)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_json = response.json()
        self.assertFalse(response_json['published'])
        self.assertEqual(response_json['author'], self.author.pk)

    def test_publish_article_user(self):
        article = mommy.make(Article, author=self.author)
        self.client.force_authenticate(self.author)
        url = reverse('articles-detail', kwargs={'pk': article.pk})
        patch_data = {
            'published': True
        }
        response = self.client.patch(url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_articles(self):
        article_count = 5
        mommy.make(Article, published=True, _quantity=article_count)
        url = reverse('articles-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), article_count)

    def test_article_retrieve(self):
        article = mommy.make(Article, published=True, views=10)
        url = reverse('articles-detail', kwargs={'pk': article.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(article.id, response.json()['id'])
        self.assertEqual(Article.objects.get(id=article.id).views, 11)

    def test_recent_articles(self):
        recent_article = mommy.make(Article, published=True)
        url = reverse('articles-recent')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0], ArticlePreviewSerializer(recent_article).data)

    def test_my_articles_count(self):
        article_count = 5
        mommy.make(Article, published=True, _quantity=article_count, author=self.author)
        self.client.force_authenticate(self.author)
        url = reverse('articles-my-articles-count')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], article_count)

    def test_my_articles_ids_list(self):
        articles_count = 5
        articles = []
        for _ in range(articles_count):
            articles.append(mommy.make(Article, published=True, author=self.author))
        self.client.force_authenticate(self.author)
        url = reverse('articles-my-articles-ids')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), articles_count)
        for article in articles:
            self.assertTrue(article.id in response.json())

    def test_edit_non_published_article(self):
        article = mommy.make(Article, author=self.author)
        self.client.force_authenticate(self.author)
        url = reverse('articles-detail', kwargs={'pk': article.pk})
        patch_data = {
            'text': 'new text here' * 5
        }
        response = self.client.patch(url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_published_article(self):
        article = mommy.make(Article, author=self.author, published=True)
        self.client.force_authenticate(self.author)
        url = reverse('articles-detail', kwargs={'pk': article.pk})
        patch_data = {
            'text': 'new text here' * 5
        }
        response = self.client.patch(url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestArticleComments(TestCase):
    def setUp(self) -> None:
        self.author = mommy.make(User)
        self.random_user = mommy.make(User)
        self.article = mommy.make(Article, author=self.author)
        self.published_article = mommy.make(Article, author=self.author, published=True)
        self.client = APIClient()

    def test_comment_create(self):
        self.client.force_authenticate(self.random_user)
        url = reverse('article-comments-list', kwargs={'article_pk': self.published_article.id})
        data = {
            'text': 'Some comment text',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ArticleComment.objects.get(id=response.json()['id']))

    def test_comment_create_non_published_article(self):
        self.client.force_authenticate(self.random_user)
        url = reverse('article-comments-list', kwargs={'article_pk': self.article.id})
        data = {
            'text': 'Some comment text',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comments_list(self):
        num_of_comments = 6
        comments = mommy.make(ArticleComment, _quantity=num_of_comments, author=self.random_user,
                              article=self.published_article)
        url = reverse('article-comments-list', kwargs={'article_pk': self.published_article.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for comment in comments:
            self.assertTrue(ArticleCommentSerializer(comment).data in response.json()['results'])

    def test_comments_edit(self):
        comment = mommy.make(ArticleComment, author=self.random_user, article=self.published_article)
        self.client.force_authenticate(self.random_user)
        url = reverse('article-comments-detail', kwargs={'article_pk': self.published_article.id, 'pk': comment.pk})
        data = {
            'text': 'New text for the comment'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ArticleComment.objects.get(id=comment.id).text, data['text'])

    def test_comment_reply(self):
        comment = mommy.make(ArticleComment, author=self.random_user, article=self.published_article)
        self.client.force_authenticate(self.random_user)
        url = reverse('article-comments-list', kwargs={'article_pk': self.published_article.id})
        data = {
            'text': 'New text for the comment',
            'reply_to': comment.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            response.json()['id'] in ArticleComment.objects.get(id=comment.id).replies.values_list('id', flat=True))

    def test_comment_reaction_like(self):
        comment = mommy.make(ArticleComment, author=self.random_user, article=self.published_article)
        self.client.force_authenticate(self.author)
        url = reverse('article-comments-like', kwargs={'article_pk': self.published_article.id, 'pk': comment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(CommentReaction.objects.filter(comment__id=comment.id, type='like'), 1)

    def test_comment_reaction_dislike(self):
        comment = mommy.make(ArticleComment, author=self.random_user, article=self.published_article)
        self.client.force_authenticate(self.author)
        url = reverse('article-comments-dislike', kwargs={'article_pk': self.published_article.id, 'pk': comment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(CommentReaction.objects.filter(comment__id=comment.id, type='dislike'), 1)

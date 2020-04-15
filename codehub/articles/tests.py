from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from articles.models import Article
from articles.serializers import ArticlePreviewSerializer


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

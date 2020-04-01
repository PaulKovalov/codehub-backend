from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from articles.models import Article


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

    def test_publish_article_admin(self):
        article = mommy.make(Article)
        admin = User.objects.create_superuser(email='root@code-hub.org', password='123456')
        self.client.force_authenticate(admin)
        url = reverse('articles-detail', kwargs={'pk': article.pk})
        patch_data = {
            'published': True
        }
        response = self.client.patch(url, patch_data)
        self.assertTrue(response.json()['published'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_publish_article_user(self):
        article = mommy.make(Article)
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

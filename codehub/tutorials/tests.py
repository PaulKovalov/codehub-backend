# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from tutorials.models import Tutorial, TutorialArticle
from tutorials.serializers import TutorialArticleSerializer, TutorialArticlePreviewSerializer, TutorialSerializer


class TestTutorials(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.author = mommy.make(User)
        self.tutorial = mommy.make(Tutorial, author=self.author)

    def test_tutorials_list(self):
        url = reverse('tutorials-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tutorial_article_create(self):
        url = reverse('tutorial-articles-list', kwargs={'tutorial_pk': self.tutorial.pk})
        data = {
            'text': 'random text here' * 10,
            'title': 'some title here'
        }
        self.client.force_authenticate(self.author)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['tutorial'], self.tutorial.id)
        self.assertTrue(TutorialArticle.objects.filter(id=response.json()['id']))

    def test_tutorial_article_publish_user(self):
        tutorial_article = mommy.make(TutorialArticle, author=self.author, published=False, tutorial=self.tutorial)
        self.client.force_authenticate(self.author)
        url = reverse('tutorial-articles-detail', kwargs={'tutorial_pk': self.tutorial.pk, 'pk': tutorial_article.pk})
        data = {
            'published': True
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_non_published_tutorial_article(self):
        tutorial_article = mommy.make(TutorialArticle, author=self.author, published=False, tutorial=self.tutorial)
        self.client.force_authenticate(self.author)
        url = reverse('tutorial-articles-detail', kwargs={'tutorial_pk': self.tutorial.pk, 'pk': tutorial_article.pk})
        data = {
            'text': 'new text here' * 5
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_published_tutorial_article(self):
        tutorial_article = mommy.make(TutorialArticle, author=self.author, published=True, tutorial=self.tutorial)
        self.client.force_authenticate(self.author)
        url = reverse('tutorial-articles-detail', kwargs={'tutorial_pk': self.tutorial.pk, 'pk': tutorial_article.pk})
        data = {
            'text': 'new text here' * 5
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tutorial_articles_list(self):
        tutorial_article = mommy.make(TutorialArticle, author=self.author, published=True, tutorial=self.tutorial)
        url = reverse('tutorial-articles-list', kwargs={'tutorial_pk': self.tutorial.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'][0], TutorialArticlePreviewSerializer(tutorial_article).data)

    def test_tutorial_article_retrieve(self):
        tutorial_article = mommy.make(TutorialArticle, author=self.author, published=True, tutorial=self.tutorial)
        url = reverse('tutorial-articles-detail', kwargs={'tutorial_pk': self.tutorial.pk, 'pk': tutorial_article.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), TutorialArticleSerializer(tutorial_article).data)

    def test_my_tutorials_list(self):
        another_tutorial = mommy.make(Tutorial)
        url = reverse('tutorials-my')
        self.client.force_authenticate(self.author)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(TutorialSerializer(another_tutorial).data not in response.json()['results'])
        self.assertTrue(TutorialSerializer(self.tutorial).data in response.json()['results'])

    def test_articles_count(self):
        num_of_articles = 5
        self.client.force_authenticate(self.author)
        mommy.make(TutorialArticle, tutorial=self.tutorial, author=self.author, _quantity=num_of_articles)
        url = reverse('tutorial-articles-my-count', kwargs={'tutorial_pk': self.tutorial.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], num_of_articles)

    def test_non_published_tutorial_retrieve_by_author(self):
        url = reverse('tutorials-detail', kwargs={'pk': self.tutorial.id})
        self.client.force_authenticate(self.author)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), TutorialSerializer(self.tutorial).data)

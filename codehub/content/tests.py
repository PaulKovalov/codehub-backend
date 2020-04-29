# Create your tests here.
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status

from accounts.models import User
from articles.models import Article
from content.models import ErrorMessage
from content.serializers import ErrorMessageSerializer
from tutorials.models import Tutorial, TutorialArticle


class TestErrorMessage(TestCase):
    def setUp(self) -> None:
        self.error_message = mommy.make(ErrorMessage, active=True)

    def test_error_messages_list(self):
        url = reverse('errormessage-list')
        response = self.client.get(url)
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0], ErrorMessageSerializer(self.error_message).data)


def current_time():
    return 0


class TestSearch(TestCase):
    def setUp(self) -> None:
        self.author = mommy.make(User)
        self.article = mommy.make(Article, published=True, author=self.author,
                                  text="sample text here to test search engine functionality")
        self.tutorial = mommy.make(Tutorial, published=True, author=self.author, preview="sample preview text here")
        self.tutorial_article = mommy.make(TutorialArticle, published=True, author=self.author,
                                           text="sample text of the tutorial article to test search engine functionality")

    @patch('content.search_engine.SearchEngine._current_time', current_time)
    def test_search(self):
        query_string = 'sample'
        url = f'{reverse("search")}?query={query_string}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

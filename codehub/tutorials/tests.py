# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework.test import APIClient

from tutorials.models import Tutorial


class TestTutorials(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_tutorials_list(self):
        tutorial = mommy.make(Tutorial)
        url = reverse('tutorials-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

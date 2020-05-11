# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status

from content.models import ErrorMessage
from content.serializers import ErrorMessageSerializer


class TestErrorMessage(TestCase):
    def setUp(self) -> None:
        self.error_message = mommy.make(ErrorMessage, active=True)

    def test_error_messages_list(self):
        url = reverse('errormessage-list')
        response = self.client.get(url)
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0], ErrorMessageSerializer(self.error_message).data)

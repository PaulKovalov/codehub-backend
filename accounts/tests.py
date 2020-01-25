from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy

from accounts.models import User


class UserCreateTest(TestCase):

    def test_create_user(self):
        email = 'test_u1@email.com'
        username = 'test_u1'
        data = {
            'username': username,
            'password': 'Qwerty123',
            'email': email
        }
        url = reverse('accounts-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.all().count(), 1)
        user = User.objects.all().first()
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)

    def test_create_invalid_email_user(self):
        email = 'test_u1email.com'
        username = 'test_u1'
        data = {
            'username': username,
            'password': 'Qwerty123',
            'email': email
        }
        url = reverse('accounts-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.all().count(), 0)

    def test_create_empty_email_user(self):
        email = ''
        username = 'test_u1'
        data = {
            'username': username,
            'password': 'Qwerty123',
            'email': email
        }
        url = reverse('accounts-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.all().count(), 0)

    def test_create_empty_username_user(self):
        email = 'test_u1@email.com'
        username = ''
        data = {
            'username': username,
            'password': 'Qwerty123',
            'email': email
        }
        url = reverse('accounts-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.all().count(), 0)


class UserRetrieveTest(TestCase):
    def setUp(self) -> None:
        mommy.make(User, )

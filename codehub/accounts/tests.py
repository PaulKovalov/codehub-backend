import urllib
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string
from model_mommy import mommy
from rest_framework import status

from accounts.models import User, ChangePasswordRequest


class UserCreateTest(TestCase):
    @patch('accounts.views.send_email_on_signup.delay')
    def test_create_user(self, mocked_send_email):
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
        mocked_send_email.assert_called_once_with(user.email)

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

    @patch('accounts.views.send_mail_password_reset.delay')
    def test_request_password_change_existing(self, mocked_send_mail):
        user = mommy.make(User)
        url = f'{reverse("accounts-request-password-change")}?email={urllib.parse.quote(user.email)}'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ChangePasswordRequest.objects.filter(email=user.email))
        request_id = ChangePasswordRequest.objects.get(email=user.email).request_id
        mocked_send_mail.assert_called_once_with(user.email,
                                                 f'{settings.HOST}/accounts/create-new-password/?request_id={request_id}')

    @patch('accounts.views.send_mail_password_reset.delay')
    def test_request_password_change_non_existing(self, mocked_send_mail):
        email = 'testemail@email.com'
        url = f'{reverse("accounts-request-password-change")}?email={urllib.parse.quote(email)}'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(ChangePasswordRequest.objects.filter(email=email))
        mocked_send_mail.assert_not_called()

    def test_request_password_change_no_email(self):
        url = reverse('accounts-request-password-change')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password(self):
        url = reverse('accounts-set-new-password')
        user = mommy.make(User)
        reset_request = ChangePasswordRequest.objects.create(email=user.email, request_id=get_random_string())
        data = {
            'request_id': reset_request.request_id,
            'password': 'newpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(authenticate(username=user.email, password=data['password']))
        self.assertFalse(ChangePasswordRequest.objects.filter(email=user.email))

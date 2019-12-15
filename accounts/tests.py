import random

from django.test import TestCase
from django.utils.crypto import get_random_string

from accounts.models import CodehubUser


def create_user(number=1):
    usernames = ['Ann', 'John', 'Yoba', 'Paul', 'Jason', 'Laura', 'Garry', 'Ronald', 'Richard', 'Matt']
    chosen_names = random.choices(usernames, k=number)
    emails = [f'{name}@email.com' for name in chosen_names]
    users = []
    for e, u in zip(chosen_names, emails):
        user_obj = CodehubUser.objects.create(username=u, email=e, view_permission_all=True)
        user_obj.set_password(get_random_string())
        users.append(user_obj)
    return users


class AccountModelTest(TestCase):

    def test_create_user(self):
        email = 'test_u1@email.com'
        username = 'test_u1'
        data = {
            'username': username,
            'password': 'Qwerty123',
            'email': email
        }
        url = '/api/v1/accounts/'
        response = self.client.post(url, data)
        rcode = response.status_code
        users_total = CodehubUser.objects.all().count()
        self.assertEqual(rcode, 201, msg=f'Expeted status code 201, got {rcode}')
        self.assertEqual(users_total, 1, msg=f'Expected 1 user in total, got {users_total}')
        user = CodehubUser.objects.all().first()
        self.assertEqual(user.email, email, msg=f'Expected user email {email}, got {user.email}')
        self.assertEqual(user.username, username, msg=f'Expected user name {username}, got {user.username}')

    def test_create_invalid_email_user(self):
        email = 'test_u1email.com'
        username = 'test_u1'
        data = {
            'username': username,
            'password': 'Qwerty123',
            'email': email
        }
        url = '/api/v1/accounts/'
        response = self.client.post(url, data)
        rcode = response.status_code
        users_total = CodehubUser.objects.all().count()
        self.assertEqual(rcode, 400, msg=f'Expeted status code 400, got {rcode}')
        self.assertEqual(users_total, 0, msg=f'Expected 0 user in total, got {users_total}')

    def test_create_empty_email_user(self):
        email = ''
        username = 'test_u1'
        data = {
            'username': username,
            'password': 'Qwerty123',
            'email': email
        }
        url = '/api/v1/accounts/'
        response = self.client.post(url, data)
        rcode = response.status_code
        users_total = CodehubUser.objects.all().count()
        self.assertEqual(rcode, 400, msg=f'Expeted status code 400, got {rcode}')
        self.assertEqual(users_total, 0, msg=f'Expected 0 user in total, got {users_total}')

    def test_create_empty_username_user(self):
        email = 'test_u1@email.com'
        username = ''
        data = {
            'username': username,
            'password': 'Qwerty123',
            'email': email
        }
        url = '/api/v1/accounts/'
        response = self.client.post(url, data)
        rcode = response.status_code
        users_total = CodehubUser.objects.all().count()
        self.assertEqual(rcode, 400, msg=f'Expeted status code 400, got {rcode}')
        self.assertEqual(users_total, 0, msg=f'Expected 0 user in total, got {users_total}')

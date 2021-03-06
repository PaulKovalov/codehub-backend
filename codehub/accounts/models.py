from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from content.models import CodehubFileField


class CodehubUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.avatar = settings.DEFAULT_AVATAR_URL
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    email = models.EmailField(blank=False, unique=True)
    objects = CodehubUserManager()
    avatar = CodehubFileField(max_length=200, upload_to='media', null=True, blank=True)


class UserLinks(models.Model):
    link = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['link', 'user'], name='Link-User constraint')
        ]


class ChangePasswordRequest(models.Model):
    email = models.EmailField()
    request_id = models.CharField(max_length=32)
    date_created = models.DateTimeField(auto_now_add=True)


class UserNotifications(models.Model):
    new_comment = models.BooleanField(default=True)
    comment_reply = models.BooleanField(default=True)
    user = models.OneToOneField(User, related_name='notifications', on_delete=models.CASCADE, null=True)

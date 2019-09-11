from django.db import models
from django.contrib.auth.models import AbstractUser

class CodehubUser(AbstractUser):
    email = models.EmailField('email address', blank=False, unique=True)

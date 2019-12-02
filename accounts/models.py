from django.contrib.auth.models import AbstractUser
from django.db import models


class CodehubUser(AbstractUser):
    email = models.EmailField('email address', blank=False, unique=True)
    # who can see my profile? All, registered or nobody
    view_permission_all = models.BooleanField(default=False)
    view_permission_registered = models.BooleanField(default=False)


class CodehubUserLinks(models.Model):
    link = models.URLField()
    user = models.ForeignKey(CodehubUser, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['link', 'user'], name='Link-User constraint')
        ]

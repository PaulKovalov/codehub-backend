from django.db import models


class ErrorMessage(models.Model):
    message = models.CharField(max_length=255)
    active = models.BooleanField(default=False)

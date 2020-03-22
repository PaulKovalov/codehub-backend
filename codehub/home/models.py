from django.db import models


class ErrorMessage(models.Model):
    """
    Error message is a message displayed at the header of the site in case site is malfunctioning
    """
    message = models.CharField(max_length=255)
    active = models.BooleanField(default=False)

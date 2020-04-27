import uuid

from django.db import models


class CodehubFileField(models.FileField):
    """
    Prepends UUID string to the filename to make it unique
    """

    def generate_filename(self, instance, filename):
        new_name = f'{uuid.uuid4()}{filename}'
        return super().generate_filename(instance, new_name)


class ImageSource(models.Model):
    name = models.CharField(max_length=150)
    file = CodehubFileField(max_length=200, upload_to='media', null=True, blank=True)

    @property
    def source_url(self):
        return self.file.url


class ErrorMessage(models.Model):
    """
    Error message is a message displayed at the header of the site in case site is malfunctioning
    """
    message = models.CharField(max_length=255)
    active = models.BooleanField(default=False)

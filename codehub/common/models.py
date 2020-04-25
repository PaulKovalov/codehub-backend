from django.db import models

from accounts.models import User


class ReactionBaseModel(models.Model):
    TYPES = (
        ('like', 'like'),
        ('dislike', 'dislike'),
    )
    type = models.CharField(choices=TYPES, max_length=8)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

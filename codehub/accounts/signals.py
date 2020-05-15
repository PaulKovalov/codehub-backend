from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User, UserNotifications


@receiver(post_save, sender=User)
def create_user_notification_objects(sender, instance, created, **kwargs):
    if created:
        UserNotifications.objects.create(user=instance)

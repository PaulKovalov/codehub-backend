from datetime import timedelta

from celery.schedules import crontab
from celery.task import periodic_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from accounts.models import ChangePasswordRequest
from codehub.celery import app


@app.task
def send_mail_on_signup(to: str):
    # TODO write some cool text here
    email_text = """Welcome to code-hub.org!\nHere you can share your knowledge in math, engineering, computer science, programming and related."""
    send_mail('Welcome to code-hub.org!', email_text, settings.EMAIL_HOST_USER, [to])


@app.task
def send_mail_password_reset(to: str, link: str):
    email_text = f'Use this link to reset the password: {link}\nThis link is valid for two hours'
    send_mail('Password reset', email_text, settings.EMAIL_HOST_USER, [to])


@periodic_task(run_every=crontab(minute='*/30'))
def clean_expired_change_password_requests():
    for request in ChangePasswordRequest.objects.all():
        if timezone.now() - request.date_created > timedelta(hours=2):
            request.delete()

from django.conf import settings
from django.core.mail import send_mail


def send_mail_new_user(to: str):
    # TODO write some cool text here
    welcome_email_text = """Welcome to code-hub.org!\nHere you can share your knowledge in math, engineering, computer science, programming and related."""
    send_mail('Welcome to code-hub.org!', welcome_email_text, settings.EMAIL_HOST_USER, [to])

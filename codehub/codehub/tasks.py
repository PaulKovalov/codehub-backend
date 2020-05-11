from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_mail_on_new_comment(to: str, from_who: str, link_to_article: str, comment_text: str, article_title: str):
    email_text = f"""User {from_who} left a comment on your article \"{article_title}\":\n{comment_text}.\nReply to it here: {link_to_article}"""
    send_mail(f'{from_who} commented your article', email_text, settings.EMAIL_HOST_USER, [to])

from django.conf import settings
from django.core.mail import send_mail

from accounts.models import User
from common.models import CommentBaseModel


def send_mail_new_user(to: str):
    # TODO write some cool text here
    email_text = """Welcome to code-hub.org!\nHere you can share your knowledge in math, engineering, computer science, programming and related."""
    send_mail('Welcome to code-hub.org!', email_text, settings.EMAIL_HOST_USER, [to])


def send_mail_on_new_comment(to: str, from_who: User, comment: CommentBaseModel):
    article_title = comment.article.title
    article_id = comment.article.id
    link_to_article = f'{settings.HOST}/articles/{article_id}/'
    email_text = f"""User {from_who.username} left a comment on your article \"{article_title}\":\n{comment.text}.\nReply to it here: {link_to_article}"""
    send_mail(f'{from_who.username} commented your article', email_text, settings.EMAIL_HOST_USER, [to])

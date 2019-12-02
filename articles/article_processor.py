"""
Codehub Article processor
Provides methods to validate data sent to server
Pavlo Kovalov 2019
"""

from django.core.exceptions import ValidationError

from codehub import config


class ArticleProcessor:

	@staticmethod
	def validate_title(title):
		if len(title) >= config.ARTICLE_TITLE_MAX_LENGTH:
			raise ValidationError("Title is too long")
		if len(title) < config.ARTICLE_TITLE_MIN_LENGTH:
			raise ValidationError("Title is too short")

	@staticmethod
	def validate_text(text):
		if len(text) >= config.ARTICLE_CONTENT_MAX_LENGTH:
			raise ValidationError("Text is too long")
		if len(text) < config.ARTICLE_CONTENT_MIN_LENGTH:
			raise ValidationError("Text is too short")

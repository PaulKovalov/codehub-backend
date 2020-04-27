from rest_framework import serializers

from content.models import ErrorMessage


class ArticleImageSerializer(serializers.Serializer):
    file = serializers.FileField()


class ErrorMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorMessage
        fields = ('message',)

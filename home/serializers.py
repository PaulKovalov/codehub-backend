from rest_framework import serializers

from home.models import ErrorMessage


class ErrorMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorMessage
        fields = ('message',)

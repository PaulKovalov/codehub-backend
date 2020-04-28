from rest_framework import serializers

from content.models import ErrorMessage


class ArticleImageSerializer(serializers.Serializer):
    file = serializers.FileField()


class ErrorMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorMessage
        fields = ('message',)


class SearchResultSerializer(serializers.Serializer):
    title = serializers.CharField()
    link = serializers.SerializerMethodField()
    match_piece = serializers.CharField()

    def get_link(self, instance):
        return instance.location

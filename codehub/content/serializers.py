from rest_framework import serializers


class ArticleImageSerializer(serializers.Serializer):
    file = serializers.FileField()

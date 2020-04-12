from rest_framework import serializers

from tutorials.models import Tutorial


class TutorialPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        read_only_fields = ('id', 'title', 'preview', 'views', 'author', 'username', 'total_views', 'date_created')
        fields = read_only_fields


class TutorialSerializer(serializers.ModelSerializer):
    table_of_content = serializers.SerializerMethodField()

    class Meta:
        model = Tutorial
        read_only_fields = ('id', 'views', 'author', 'username', 'total_views', 'date_created', 'table_of_content')
        fields = ('title', 'preview') + read_only_fields

    def get_table_of_content(self, instance):
        return instance.articles.filter(published=True).order_by('date_created').values_list('title', 'id')

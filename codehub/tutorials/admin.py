# Register your models here.
from django.contrib import admin

from tutorials.models import Tutorial, TutorialArticle


class TutorialAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'date_created', 'views', 'total_views', 'last_modified')
    list_display = ('id', 'title', 'author', 'views', 'published', 'date_created')
    list_filter = ('id', 'author', 'published')
    fieldsets = [
        ('Tutorial information', {'fields': ['id', 'title', 'preview', 'author', 'views', 'total_views', 'published']}),
        ('Date information', {'fields': ['date_created', 'last_modified']}),
    ]


class TutorialArticleAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'views', 'last_modified')
    list_display = ('id', 'title', 'author', 'views', 'published')


admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(TutorialArticle, TutorialArticleAdmin)

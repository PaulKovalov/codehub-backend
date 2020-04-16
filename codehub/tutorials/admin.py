# Register your models here.
from django.contrib import admin

from tutorials.models import Tutorial, TutorialArticle


def make_published(modeladmin, request, queryset):
    for tutorial in queryset:
        for article in tutorial.articles.all():
            article.published = True
            article.save(update_fields=['published'])
        tutorial.published = True
        tutorial.save(update_fields=['published'])


class TutorialAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'date_created', 'views', 'total_views', 'last_modified', 'articles')
    list_display = ('id', 'title', 'author', 'views', 'published', 'date_created')
    list_filter = ('id', 'author', 'published')
    fieldsets = [
        ('Tutorial information',
         {'fields': ['id', 'title', 'preview', 'author', 'views', 'total_views', 'published', 'articles']}),
        ('Date information', {'fields': ['date_created', 'last_modified']}),
    ]

    def articles(self, obj):
        return [a.id for a in obj.articles.all()]

    actions = [make_published]


class TutorialArticleAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'views', 'last_modified')
    list_display = ('id', 'title', 'author', 'views', 'published')


admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(TutorialArticle, TutorialArticleAdmin)

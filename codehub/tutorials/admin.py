# Register your models here.
from django.contrib import admin

from tutorials.models import Tutorial, TutorialArticle


class TutorialAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'date_created', 'views', 'total_views')
    list_display = ('id', 'title', 'author', 'views', 'published', 'date_created', 'articles')
    list_filter = ('id', 'author', 'published')
    fieldsets = [
        ('Tutorial information', {'fields': ['id', 'title', 'text', 'author', 'views', 'total_views', 'published']}),
        ('Date information', {'fields': ['date_created']}),
    ]


admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(TutorialArticle)

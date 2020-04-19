from django.contrib import admin

from .models import Article, ArticleComment


class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'date_created', 'views', 'last_modified')
    list_display = ('id', 'title', 'author', 'views', 'published', 'date_created')
    list_filter = ('id', 'author', 'published')
    fieldsets = [
        ('Article content information', {'fields': ['id', 'title', 'text', 'author', 'views', 'published']}),
        ('Date information', {'fields': ['date_created', 'last_modified']}),
    ]


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment)

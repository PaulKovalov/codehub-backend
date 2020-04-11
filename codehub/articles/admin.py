from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'date_created', 'views')
    list_display = ('id', 'title', 'author', 'views', 'published', 'date_created')
    list_filter = ('id', 'author', 'published')
    fieldsets = [
        ('Article content information', {'fields': ['id', 'title', 'text', 'author', 'views', 'published']}),
        ('Date information', {'fields': ['date_created']}),
    ]


admin.site.register(Article, ArticleAdmin)

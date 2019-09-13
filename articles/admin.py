from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'views', 'published')
    list_filter = ('id', 'author', 'published')
    fieldsets = [
        (None, {'fields': ['title', 'text', 'author', 'views', 'published']}),
        ('Date information', {'fields': ['date_created']}),
    ]


admin.site.register(Article, ArticleAdmin)

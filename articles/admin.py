from .models import Article
from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    fields = ['id','title','author','published','views','date_created']

admin.site.register(Article, ArticleAdmin)

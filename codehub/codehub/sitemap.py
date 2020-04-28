from django.contrib.sitemaps import Sitemap

from articles.models import Article
from tutorials.models import Tutorial, TutorialArticle


class CodeHubSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        items = []
        for article in Article.objects.filter(published=True):
            items.append(article)
        for tutorial in Tutorial.objects.filter(published=True):
            items.append(tutorial)
        for tutorial_article in TutorialArticle.objects.filter(published=True):
            items.append(tutorial_article)

        return items

    def location(self, obj):
        return obj.location

    def lastmod(self, obj):
        return obj.last_modified

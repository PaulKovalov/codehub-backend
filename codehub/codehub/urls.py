from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from codehub.sitemap import CodeHubSitemap

sitemaps = dict(content=CodeHubSitemap)

api_urls = [
    path('', include('articles.urls')),
    path('', include('accounts.urls')),
    path('', include('tutorials.urls')),
    path('', include('content.urls'))
]

urlpatterns = [
    path('api/v1/', include(api_urls)),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]

"""
codehub URL Configuration
Pavlo Kovalov 2019
"""
from django.contrib import admin
from django.urls import path, include

api_urls = [
    path('', include('articles.urls')),
    path('', include('accounts.urls')),
    path('', include('home.urls')),
    path('', include('tutorials.urls'))
]

urlpatterns = [
    path('api/v1/', include(api_urls)),
    path('admin/', admin.site.urls),
]

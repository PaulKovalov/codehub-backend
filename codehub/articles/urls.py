"""
Codehub Article API urls
Pavlo Kovalov 2019
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ArticlesViewSet

router = DefaultRouter()
router.register(r'articles', ArticlesViewSet, basename='articles')

urlpatterns = [
    path('', include(router.urls)),
]

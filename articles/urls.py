"""
Codehub Article API urls
Pavlo Kovalov 2019
"""
from .views import ArticlesViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'articles', ArticlesViewSet, basename='articles')

urlpatterns = [
	path('', include(router.urls)),
]
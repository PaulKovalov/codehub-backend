from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from articles import views

router = SimpleRouter()
router.register(r'articles', views.ArticlesViewSet, basename='articles')

comments_router = NestedSimpleRouter(router, 'articles', lookup='article')
comments_router.register('comments', views.ArticleCommentsViewSet, basename='article-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(comments_router.urls))
]

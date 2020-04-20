from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from tutorials import views

router = SimpleRouter()
router.register('tutorials', views.TutorialsViewSet, basename='tutorials')

articles_router = NestedSimpleRouter(router, 'tutorials', lookup='tutorial')
articles_router.register('articles', views.TutorialArticlesViewSet, basename='tutorial-articles')

comments_router = NestedSimpleRouter(articles_router, 'articles', lookup='article')
comments_router.register('comments', views.TutorialArticleCommentsViewSet, basename='tutorial_article-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(articles_router.urls)),
    path('', include(comments_router.urls))
]

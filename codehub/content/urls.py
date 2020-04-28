from django.urls import path, include
from rest_framework.routers import SimpleRouter

from content import views

router = SimpleRouter()
router.register(r'errors', views.ErrorMessagesViewSet)

urlpatterns = [
    path('content/uploads/', views.UploadArticleImageView.as_view()),
    path('get-csrf', views.get_csrf),
    path('search/', views.SearchView.as_view(), name='search'),
    path('', include(router.urls)),
]

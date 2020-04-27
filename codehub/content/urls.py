from django.urls import path, include
from rest_framework.routers import SimpleRouter

from content import views

router = SimpleRouter()
router.register(r'errors', views.ErrorMessagesViewSet)

urlpatterns = [
    path('content/uploads/', views.UploadArticleImageView.as_view()),
    path('get-csrf', views.get_csrf),
    path('', include(router.urls)),
]

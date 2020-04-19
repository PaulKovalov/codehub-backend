from django.urls import path, include
from rest_framework.routers import DefaultRouter

from home import views

router = DefaultRouter()
router.register(r'errors', views.ErrorMessagesViewSet)

urlpatterns = [
    path('get-csrf', views.get_csrf),
    path('', include(router.urls)),
]

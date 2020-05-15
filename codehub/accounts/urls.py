from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from accounts import views

router = SimpleRouter()
router.register(r'accounts', views.UserViewSet, basename='accounts')

notifications_router = NestedSimpleRouter(router, 'accounts', lookup='account')
notifications_router.register('notifications', views.UserNotificationsViewSet, basename='notifications')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(notifications_router.urls))
]

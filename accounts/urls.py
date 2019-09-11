"""
Codehub Accounts API urls
Pavlo Kovalov 2019
"""

from .views import UserViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'accounts', UserViewSet, basename='accounts')

urlpatterns = [
    path('accounts/api-auth/', obtain_auth_token, name='api_auth'),
    path('', include(router.urls)),
]
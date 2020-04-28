
from django.contrib.auth import login, logout
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import User
from accounts.permissions import UsersPermissions
from accounts.serializers import UserSerializer, UserAuthenticationSerializer
from common.email_utils import send_mail_new_user


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_class = [UsersPermissions]
    queryset = User.objects.all()

    def perform_create(self, serializer):
        new_user = serializer.save()
        send_mail_new_user(new_user.email)
        login(self.request, new_user)

    @action(methods=['POST'], detail=False, serializer_class=UserAuthenticationSerializer)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        login(request, validated_data['account'])
        return Response()

    @action(methods=['GET'], detail=False)
    def logout(self, request):
        logout(request)
        return Response()

    def get_object(self):
        if self.kwargs[self.lookup_field] == 'me' and self.request.user.is_authenticated:
            user = self.request.user
            self.check_object_permissions(self.request, user)
            return user
        return super().get_object()

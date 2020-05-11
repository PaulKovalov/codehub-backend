from django.conf import settings
from django.contrib.auth import login, logout
from django.utils.crypto import get_random_string
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import User, ChangePasswordRequest
from accounts.permissions import UsersPermissions
from accounts.serializers import UserSerializer, UserAuthenticationSerializer, ChangePasswordRequestSerializer
from accounts.tasks import send_email_on_signup, send_mail_password_reset


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
        send_email_on_signup.delay(new_user.email)
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

    @action(methods=['POST'], detail=False, permission_class=AllowAny, url_name='request-password-change',
            url_path='request-password-change')
    def request_password_change(self, request):
        email = request.query_params.get('email')
        if email is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email):
            request_id = get_random_string(length=32)
            ChangePasswordRequest.objects.delete(email=email)
            ChangePasswordRequest.objects.create(email=email, request_id=request_id)
            url = f'{settings.HOST}/accounts/create-new-password/'
            send_mail_password_reset.delay(email, url)
        return Response()

    @action(methods=['POST'], detail=False, permission_class=AllowAny, url_name='set-new-password',
            url_path='set-new-password')
    def set_new_password(self, request):
        serializer = ChangePasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        new_password = serializer.validated_data['password']
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return Response()

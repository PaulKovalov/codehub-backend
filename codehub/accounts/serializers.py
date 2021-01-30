from django.conf import settings
from django.contrib.auth import authenticate
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, ChangePasswordRequest, UserNotifications


class UserSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'avatar')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_avatar(self, value):
        if value.size > settings.MAX_AVATAR_SIZE:
            raise ValidationError(f'File size can not exceed {settings.MAX_AVATAR_SIZE} bytes')
        return value


class UserAuthenticationSerializer(serializers.Serializer):
    WRONG_CREDENTIALS = 'Invalid email or password'
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, attrs):
        email = attrs['email'].lower()
        password = attrs['password']
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(self.WRONG_CREDENTIALS)
        attrs['account'] = user
        return attrs


class ViewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'articles', 'tutorials')


class ChangePasswordRequestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = ChangePasswordRequest
        fields = ('request_id', 'password')

    def validate(self, attrs):
        if not ChangePasswordRequest.objects.filter(request_id=attrs['request_id']):
            raise serializers.ValidationError('Request id not found')
        return attrs


class UserNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotifications
        fields = ('new_comment', 'comment_reply', 'id')

from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User, ChangePasswordRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


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
        fields = ('email', 'request_id', 'password')

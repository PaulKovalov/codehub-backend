from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CodehubUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodehubUser
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        user = CodehubUser(
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
        password = attrs['passwor']
        account = authenticate(request=self.context['request'], email=email, password=password)
        if account is None:
            raise serializers.ValidationError(self.WRONG_CREDENTIALS)
        attrs['account'] = account
        return attrs


class ViewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodehubUser
        fields = ('id', 'username', 'articles', 'tutorials')

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

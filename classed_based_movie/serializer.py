from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username):
        if User.objects.filter(usrename=username).exists():
            raise ValidationError('Username already exists')
        return username

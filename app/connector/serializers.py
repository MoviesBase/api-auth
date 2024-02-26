import re

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from connector.models import UserModel


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if (username or email) and password:
            if username:
                user = authenticate(username=username, password=password)
            else:
                user = authenticate(email=email, password=password)

            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError(
                'Must include username or email and password',
            )

        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = '__all__'
        read_only_fields = ('email_verified',)

    def validate_password(self, value):
        # Check if password has at least 8 characters
        if len(value) < 8:
            raise serializers.ValidationError(
                'Password must be at least 8 characters long.'
            )

        # Check if password has at least one uppercase letter
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                'Password must contain at least one uppercase letter.'
            )

        # Check if password has at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):  # noqa: E501
            raise serializers.ValidationError(
                'Password must contain at least one special character.'
            )

        return value

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        # fields = '__all__'
        exclude = [
            'user_permissions',
            'groups',
            'is_admin',
            'is_staff',
            'is_superuser',
            'last_login',
            'date_joined',
        ]

    def update(self, instance, validated_data):
        # Check if email is being updated
        if 'email' in validated_data:
            # Set email_verified to False if email is updated
            validated_data['email_verified'] = False

        return super().update(instance, validated_data)

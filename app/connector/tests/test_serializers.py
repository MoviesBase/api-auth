from django.test import TestCase
from rest_framework import serializers

from connector.models import UserModel
from connector.serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


class UserLoginSerializerTest(TestCase):
    def tearDown(self):
        # Clean up created objects
        UserModel.objects.all().delete()

    def test_valid_login(self):
        user = UserModel.objects.create_user(
            username='testuser', password='12345'
        )
        data = {'username': 'testuser', 'password': '12345'}
        serializer = UserLoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(serializer.validated_data['user'], user)

    def test_invalid_login(self):
        data = {'username': 'nonexistent', 'password': 'invalid'}
        serializer = UserLoginSerializer(data=data)
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_missing_credentials(self):
        data = {'username': 'testuser'}
        serializer = UserLoginSerializer(data=data)
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)


class UserRegistrationSerializerTest(TestCase):
    def test_valid_registration(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Test1234!',
            'first_name': 'name',
            'last_name': 'last_name',
        }
        serializer = UserRegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')

    def test_invalid_password(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'weak',
        }
        serializer = UserRegistrationSerializer(data=data)
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)


class UserSerializerTest(TestCase):
    def tearDown(self):
        # Clean up created objects
        UserModel.objects.all().delete()

    def test_email_update(self):
        user = UserModel.objects.create(
            username='testuser', email='old@example.com'
        )
        data = {'email': 'new@example.com'}
        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()
        self.assertEqual(updated_user.email, 'new@example.com')
        self.assertFalse(updated_user.email_verified)

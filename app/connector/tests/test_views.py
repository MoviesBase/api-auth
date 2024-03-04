from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from connector.models import UserModel

User = get_user_model()


class UserLoginViewTest(TestCase):
    URL_NAME_LOGIN = 'api_login'

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

    def test_valid_login(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(reverse(self.URL_NAME_LOGIN), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Access Token', response.data)
        self.assertIn('User Token', response.data)
        token = AccessToken(response.data['Access Token'])
        self.assertEqual(token['user_id'], self.user.id)

    def test_invalid_login(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(reverse(self.URL_NAME_LOGIN), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_credentials(self):
        data = {}
        response = self.client.post(reverse(self.URL_NAME_LOGIN), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_access(self):
        # Make a request without authentication credentials
        response = self.client.post(reverse(self.URL_NAME_LOGIN), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserRegistrationViewTest(TestCase):
    URL_NAME_REGISTRATION = 'api_register'

    def setUp(self):
        self.client = APIClient()

    def test_valid_registration(self):
        data = {
            'username': 'testuser',
            'password': 'testpassworD!',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }
        response = self.client.post(reverse(self.URL_NAME_REGISTRATION), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserModel.objects.filter(username='testuser').exists())

    def test_invalid_registration(self):
        # Missing required fields
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com',
        }
        response = self.client.post(reverse(self.URL_NAME_REGISTRATION), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            UserModel.objects.filter(username='testuser').exists()
        )

    def test_duplicate_username(self):
        # Attempt to register with an existing username
        UserModel.objects.create_user(
            username='existinguser', password='testpassword'
        )
        data = {
            'username': 'existinguser',
            'password': 'testpassword',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
        }
        response = self.client.post(reverse(self.URL_NAME_REGISTRATION), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            UserModel.objects.filter(email='newuser@example.com').exists()
        )

    def test_duplicate_email(self):
        # Attempt to register with an existing email
        UserModel.objects.create_user(
            username='existinguser',
            password='testpassword',
            email='existing@example.com',
        )
        data = {
            'username': 'newuser',
            'password': 'testpassword',
            'email': 'existing@example.com',
            'first_name': 'New',
            'last_name': 'User',
        }
        response = self.client.post(reverse(self.URL_NAME_REGISTRATION), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(UserModel.objects.filter(username='newuser').exists())


class UserViewSetTest(TestCase):
    USER_NAME_URL = 'user'

    def setUp(self):
        self.client = APIClient()
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='Testpassword1!',
            first_name='name',
            last_name='lastname',
            email='email@email.com',
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_update_user(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'first_name': 'Updated',
            'last_name': 'User',
        }
        response = self.client.put(reverse(self.USER_NAME_URL), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        updated_user = UserModel.objects.get(username='testuser')
        self.assertEqual(updated_user.first_name, 'Updated')

    def test_retrieve_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse(self.USER_NAME_URL))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_delete_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse(self.USER_NAME_URL))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            UserModel.objects.filter(username='testuser').exists()
        )

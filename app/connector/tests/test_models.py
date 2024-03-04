from django.test import TestCase

from connector.models import UserModel


class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
        }

    def tearDown(self):
        # Clean up created objects
        UserModel.objects.all().delete()

    def test_create_user(self):
        user = UserModel.objects.create_user(**self.user_data)
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertFalse(user.email_verified)

    def test_create_superuser(self):
        superuser = UserModel.objects.create_superuser(
            username='admin', email='admin@example.com', password='password'
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

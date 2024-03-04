from unittest.mock import patch

from django.test import TestCase

from connector.models import UserModel
from connector.operations import EmailVerificationOperations, UserOperations


class UserOperationsTest(TestCase):
    def setUp(self):
        self.user_data = {'username': 'testuser', 'email': 'test@example.com'}
        self.user_instance = UserModel.objects.create(
            username='existing_user', email='existing@example.com'
        )

    def tearDown(self):
        # Clean up created objects
        UserModel.objects.all().delete()

    def test_update_user(self):
        new_username = 'newusername'
        data = {'username': new_username}
        context = {}
        operation = UserOperations()
        operation.update_user(data, self.user_instance, context)

        # Reload the user instance from the database
        updated_user = UserModel.objects.get(id=self.user_instance.id)
        self.assertEqual(updated_user.username, new_username)

    def test_get_user_instance(self):
        user_id = self.user_instance.id
        operation = UserOperations()
        result = operation.get_user_instance(user_id)
        self.assertEqual(result, self.user_instance)

    def test_delete_user_record(self):
        operation = UserOperations()
        operation.delete_user_record(self.user_instance)
        with self.assertRaises(UserModel.DoesNotExist):
            UserModel.objects.get(id=self.user_instance.id)


class EmailVerificationOperationsTest(TestCase):
    @patch('connector.operations.send_mail')
    @patch('connector.operations.random.choices')
    def test_send_otp_to_email(self, mock_choices, mock_send_mail):
        mock_choices.return_value = ['1', '2', '3', '4', '5', '6']
        email = 'test@example.com'
        operation = EmailVerificationOperations()
        otp = operation.send_otp_to_email(email)
        mock_send_mail.assert_called_once_with(
            'OTP for Email Verification',
            'Your OTP is: 123456',
            'test',
            ['test@example.com'],
            fail_silently=False,
        )
        self.assertEqual(otp, '123456')

    def test_generate_otp_default_length(self):
        operation = EmailVerificationOperations()
        otp = operation.generate_otp()
        self.assertEqual(len(otp), 6)

    def test_generate_otp_custom_length(self):
        operation = EmailVerificationOperations()
        otp = operation.generate_otp(length=8)
        self.assertEqual(len(otp), 8)

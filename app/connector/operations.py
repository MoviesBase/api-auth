import logging
import random
import string

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from rest_framework.exceptions import APIException, NotFound

from connector import serializers
from connector.models import UserModel

logger = logging.getLogger(__name__)


class UserOperations:
    serializer_class = serializers.UserSerializer

    def update_user(self, user_data, user_instance, context):
        """
        Updates user information in database

        user_data: User data
        context: {'contect':request}
        user_instance: user instance on given id
        """
        try:
            serializer = self.serializer_class(
                user_instance, data=user_data, context=context, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except UserModel.DoesNotExist as e:
            raise NotFound(e)
        except ValidationError as e:
            raise ValidationError(e)
        except APIException as e:
            raise APIException(e)

    def get_user_instance(self, username):
        """
        Returns user from the database on given ID
        Parameters: user_id
        """
        try:
            user = UserModel.objects.get(pk=username)
            return user
        except UserModel.DoesNotExist as e:
            raise NotFound(e)
        except ValidationError as e:
            raise ValidationError(e)
        except APIException as e:
            raise APIException(e)

    def delete_user_record(self, user_instance):
        """
        Deletes user record in database
        Parameters: user_instance  (user instance on given id)
        """
        try:
            user_instance.delete()
        except UserModel.DoesNotExist as e:
            raise NotFound(e)
        except ValidationError as e:
            raise ValidationError(e)
        except APIException as e:
            raise APIException(e)


class EmailVerificationOperations:
    # Generate OTP
    def generate_otp(self, length=6):
        return ''.join(random.choices(string.digits, k=length))

    # Send OTP via Email
    def send_otp_to_email(self, email):
        otp = self.generate_otp()

        # Simulate sending OTP to the user's email
        send_mail(
            'OTP for Email Verification',
            f'Your OTP is: {otp}',
            settings.EMAIL_USER_HOST,
            [email],
            fail_silently=False,
        )

        return otp

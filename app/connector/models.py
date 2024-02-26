from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class UserModel(AbstractUser):
    # Restrict username to alphanumeric characters, underscores or hyphens
    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_-]+$',
        message='Username must contain only alphanumeric characters.',
    )

    is_admin = models.BooleanField(default=False)
    username = models.CharField(
        primary_key=True,
        max_length=50,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': 'A user with that username already exists.',
        },
        help_text='unique identifier of the user',
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    second_last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)

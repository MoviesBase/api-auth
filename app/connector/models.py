from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models


class UserModel(AbstractUser):
    id = models.AutoField(
        primary_key=True,
        help_text='A unique identifier for each movie',
    )

    # Restrict username to alphanumeric characters, underscores or hyphens
    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_-]+$',
        message='Username must contain only alphanumeric characters.',
    )

    is_admin = models.BooleanField(default=False)
    username = models.CharField(
        unique=True,
        max_length=50,
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
    objects = UserManager()

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)

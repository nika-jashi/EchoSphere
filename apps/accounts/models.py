from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)


class CustomAccountManager(BaseUserManager):
    """ Manager For User """

    def create_user(self, email, password, **extra_fields):
        """ Create and save a User with the given email and password. """

        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """ Create and save a SuperUser with the given email and password. """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is False:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is False:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomAccount(AbstractUser):
    """ User In The System """

    email = models.EmailField(
        max_length=255,
        unique=True,
        error_messages={'unique': 'User With This Email Is Already Registered'})
    username = models.CharField(unique=True, max_length=38)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomAccountManager()

    def __str__(self):
        return self.username

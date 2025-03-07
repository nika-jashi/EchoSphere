import os
import uuid
from enum import Enum

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


def profile_picture_file_path(instance, filename):
    """ Generate file path for new recipe image """
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'users', filename)


class Profile(models.Model):
    user = models.OneToOneField(CustomAccount, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=32, null=True)
    date_of_birth = models.DateField(null=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to=profile_picture_file_path, null=True)
    GENDER_CHOICES = (
        ('U', _('Unknown')),
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Others')),
    )

    gender = models.CharField(
        choices=GENDER_CHOICES,
        default='U',  # Start with U (Unknown)
        null=True,
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Follow(models.Model):
    """ Model to represent a user following another user """

    follower = models.ForeignKey(
        CustomAccount, related_name='following', on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        CustomAccount, related_name='followers', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"
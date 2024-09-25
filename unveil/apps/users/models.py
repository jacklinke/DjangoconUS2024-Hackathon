"""Models for the unveil users app."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserAccount(AbstractUser):
    """Model for custom user accounts."""

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    def __str__(self):
        return self.email

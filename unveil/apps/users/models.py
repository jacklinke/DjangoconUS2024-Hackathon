"""Models for the unveil users app."""

import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserAccountManager(BaseUserManager):
    """Manager for user accounts."""

    def create_user(self, email, name, password=None):
        """Create a new user account."""
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create a new superuser account."""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    """Model for custom user accounts."""

    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, default="None")

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        """Return string representation of our user"""
        return self.email

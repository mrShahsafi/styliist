import uuid

from django.contrib.auth.models import (
    PermissionsMixin,
    AbstractBaseUser,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import CommonBaseModel
from ..managers import BaseUserManager


class BaseUser(CommonBaseModel, AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
    )

    first_name = models.CharField(
        _("first name"),
        max_length=150,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        null=True,
        blank=True,
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    objects = BaseUserManager()

    @property
    def full_name(self):
        data = f"{self.first_name or ''} {self.last_name or ''}"
        return data

    def __str__(self):
        return self.email

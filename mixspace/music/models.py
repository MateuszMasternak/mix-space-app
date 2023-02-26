from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, FileExtensionValidator


class CustomAbstractUser(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    avatar = models.ImageField(
        upload_to="media/core/avatars",
        null=True
    )
    is_active = models.BooleanField(
        default=False
    )

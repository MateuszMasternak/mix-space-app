from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, FileExtensionValidator
from mixspace.settings import AUTH_USER_MODEL


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


class Follow(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following"
    )
    follower = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="follower"
    )


class Track(models.Model):
    artist = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="artist"
    )
    title = models.CharField(
        max_length=32,
        validators=[MinLengthValidator(4)]
    )
    genre = models.CharField(
        max_length=256
    )
    time_added = models.DateTimeField(
        auto_now_add=True
    )
    file = models.FileField(
        upload_to="media/core/audio",
        validators=[
            FileExtensionValidator(allowed_extensions=["wav"])
        ]
    )


class Like(models.Model):
    track = models.ForeignKey(
        "Track",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="liker"
    )

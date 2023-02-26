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


class Set(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artists')
    title = models.CharField(max_length=32, validators=[MinLengthValidator(4)])
    genre = models.CharField(max_length=256)
    time_added = models.DateTimeField()
    file = models.FileField(upload_to='music/media/audio', validators=[
        FileExtensionValidator(allowed_extensions=['wav'])
    ])
    like = models.ManyToManyField(User, related_name='likes')

    def serialize(self):
        return {
            'artist': self.artist.username,
            'title': self.title,
            'genre': self.genre,
            'time_added': self.time_added.strftime('%d/%m/%Y, %H:%M'),
            'file': self.file.path
        }

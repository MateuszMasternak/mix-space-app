from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, FileExtensionValidator


class User(AbstractUser):
    email_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='music/media/avatars', default='default.jpg')

    def serialize(self):
        return {
            'username': self.username,
            'avatar': self.avatar.path
        }


class Set(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=32, validators=[MinLengthValidator(4)])
    genre = models.CharField(max_length=256)
    time_added = models.DateTimeField()
    file = models.FileField(upload_to='music/media/audio', validators=[
        FileExtensionValidator(allowed_extensions=['wav'])
    ])

    def serialize(self):
        return {
            'artist': self.artist.username,
            'title': self.title,
            'genre': self.genre,
            'time_added': self.time_added.strftime('%d/%m/%Y, %H:%M'),
            'file': self.file.path
        }

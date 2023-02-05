from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, FileExtensionValidator


class User(AbstractUser):
    avatar = models.ImageField(upload_to='music/media/avatars', null=True)
    # following = models.ManyToManyField('self', symmetrical=False, related_name='follow')
    # followed = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    def serialize(self):
        return {
            'username': self.username,
            'avatar': self.avatar.path
        }


class Follows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE())
    date_followed = models.DateTimeField(auto_now_add=True)


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

import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import ImageFieldFile

from core.models import Follow, Like, Track
from fixtures import sample_user, second_sample_user, \
    sample_track_sample_user as track_1


def test_user_model(sample_user, django_user_model):
    user = django_user_model.objects.get(pk=1)
    user.avatar = SimpleUploadedFile('file.png', b'file_content',
                                            content_type='image/png')
    assert user.username == 'TestUsername'
    assert user.email == 'testemail@example.com'
    assert user.password != 'TestPassword123!'
    assert user.is_active == True
    assert user.avatar.file is not None

def test_follow_model(sample_user, second_sample_user):
    Follow.objects.create(user=sample_user, follower=second_sample_user)
    follow = Follow.objects.get(pk=1)
    assert follow.user == sample_user
    assert follow.follower != sample_user

def test_track_model(sample_user, track_1):
    track = Track.objects.get(pk=1)
    assert track.artist == sample_user
    assert track.title == 'TestTitle'
    assert track.genre == 'Test'

def test_like_model(second_sample_user, track_1):
    Like.objects.create(track=track_1, user=second_sample_user)
    like = Like.objects.get(pk=1)
    assert like.track == track_1
    assert like.user == second_sample_user

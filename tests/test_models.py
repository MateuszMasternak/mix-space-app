import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import ImageFieldFile

from core.models import Follow
from fixtures import sample_user, second_sample_user, \
    sample_track_sample_user as track_1


def test_user_model(sample_user):
    sample_user.avatar = SimpleUploadedFile('file.png', b'file_content',
                                            content_type='image/png')

    assert sample_user.username == 'TestUsername'
    assert sample_user.email == 'testemail@example.com'
    assert sample_user.password != 'TestPassword123!'
    assert sample_user.is_active == True
    assert sample_user.avatar.file is not None

def test_follow_model(sample_user, second_sample_user):
    follow = Follow.objects.create(user=sample_user, follower=second_sample_user)
    assert follow.user == sample_user
    assert follow.follower != sample_user

def test_follow_track(sample_user, track_1):
    assert track_1.artist == sample_user
    assert track_1.title == 'TestTitle'
    assert track_1.genre == 'Test'
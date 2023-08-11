import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from core.models import Track


@pytest.fixture
def sample_user(django_user_model):
    username = 'TestUsername'
    email = 'testemail@example.com'
    password = 'TestPassword123!'
    return django_user_model.objects.create_user(username=username,
                                                 email=email,
                                                 password=password)
@pytest.fixture
def second_sample_user(django_user_model):
    username = 'TestUsername2'
    email = 'testemail2@example.com'
    password = 'TestPassword123!'
    return django_user_model.objects.create_user(username=username,
                                                 email=email,
                                                 password=password)

@pytest.fixture
def sample_track_sample_user(sample_user):
    file = SimpleUploadedFile('file.wav', b'file_content',
                              content_type='audio/wav')
    return Track.objects.create(artist=sample_user,
                                title='TestTitle',
                                genre='Test',
                                file=file)

@pytest.fixture
def sample_track_second_sample_user(second_sample_user):
    file = SimpleUploadedFile('file.wav', b'file_content',
                              content_type='audio/wav')
    return Track.objects.create(artist=second_sample_user,
                                title='TestTitle2',
                                genre='Test',
                                file=file)
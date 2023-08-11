import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from simple_assert_status_codes import assert_status_codes as simple_assert
from fixtures import sample_user, sample_track_sample_user
from fixtures import second_sample_user, sample_track_second_sample_user

def test_upload_view(client, sample_user):
    client.force_login(sample_user)
    url = reverse('upload')

    response = client.get(url)
    assert response.status_code == 200

    # Correct file format
    file = SimpleUploadedFile('file.wav', b'file_content',
                              content_type='audio/wav')
    response = client.post(url, {'file': file}, format='multipart')
    assert response.status_code == 302

    # Wrong file format
    file = SimpleUploadedFile('file.wav', b'file_content',
                              content_type='audio/mp3')
    response = client.post(url, {'file': file}, format='multipart')
    assert response.status_code == 302

    response = client.put(url)
    assert response.status_code == 501

    response = client.patch(url)
    assert response.status_code == 501

    response = client.delete(url)
    assert response.status_code == 501

def test_liked_view(client, sample_user):
    client.force_login(sample_user)
    url = reverse('liked')
    simple_assert(client, url, get=200)

def test_follow_view(client, sample_user):
    client.force_login(sample_user)
    url = reverse('follow', kwargs={'username': 'test'})
    simple_assert(client, url, get=404, post=404)

def test_follow_view_with_second_user(client, sample_user, second_sample_user):
    client.force_login(sample_user)
    url = reverse('follow', kwargs={'username': 'TestUsername2'})
    simple_assert(client, url, get=200, post=200)

def test_following_view(client, sample_user):
    client.force_login(sample_user)
    url = reverse('following')
    simple_assert(client, url, get=200)

def test_avatar_upload_view(client, sample_user):
    client.force_login(sample_user)
    url = reverse('avatar_upload')

    response = client.get(url)
    assert response.status_code == 405

    file = SimpleUploadedFile('file.png', b'file_content',
                              content_type='image/png')
    response = client.post(url, {'avatar': file}, format='multipart')
    assert response.status_code == 302

    response = client.put(url)
    assert response.status_code == 501

    response = client.patch(url)
    assert response.status_code == 501

    response = client.delete(url)
    assert response.status_code == 501

def test_delete_view_author_logged_in(client, sample_user,
                                      sample_track_sample_user):
    print(sample_track_sample_user.id)
    client.force_login(sample_user)
    url = reverse('delete', kwargs={'pk': 2})
    simple_assert(client, url, get=405, post=200)

def test_delete_view_other_user_logged_in(client, sample_user,
                                          sample_track_second_sample_user):
    print(sample_track_second_sample_user.id)
    client.force_login(sample_user)
    url = reverse('delete', kwargs={'pk': 3})
    simple_assert(client, url, get=405, post=401)

def test_delete_view_not_existing_track(client, sample_user):
    client.force_login(sample_user)
    url = reverse('delete', kwargs={'pk': 1})
    simple_assert(client, url, get=405, post=404)

def test_log_out_view(client, sample_user):
    client.force_login(sample_user)
    url = reverse('log_out')
    simple_assert(client, url, _all=302)
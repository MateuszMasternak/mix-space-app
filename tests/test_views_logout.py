import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_index_view(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200

def test_sign_up_view(client):
    url = reverse('sign_up')
    response = client.get(url)
    assert response.status_code == 200

def test_log_in_view(client):
    url = reverse('log_in')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_player_view(client):
    url = reverse('player', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 200

def test_log_out_view(client):
    url = reverse('log_out')
    response = client.get(url)
    assert response.status_code == 302

def test_upload_view(client):
    url = reverse('upload')
    response = client.get(url)
    assert response.status_code == 302

def test_liked_view(client):
    url = reverse('liked')
    response = client.get(url)
    assert response.status_code == 302

def test_follow_view(client):
    url = reverse('follow', kwargs={'username': 'test'})
    response = client.get(url)
    assert response.status_code == 302

def test_following_view(client):
    url = reverse('following')
    response = client.get(url)
    assert response.status_code == 302

def test_avatar_upload_view(client):
    url = reverse('avatar_upload')
    response = client.get(url)
    assert response.status_code == 302

def test_delete_view(client):
    url = reverse('delete', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 302
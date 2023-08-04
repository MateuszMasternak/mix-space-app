import pytest

from django.urls import reverse
from simple_assert_status_codes import assert_status_codes

@pytest.mark.django_db
def test_index_view(client):
    url = reverse('index')
    assert_status_codes(client, url, get=200)

def test_sign_up_view(client):
    url = reverse('sign_up')
    response = client.get(url)
    assert response.status_code == 200
    # assert_status_codes(client, url, get=200)

def test_log_in_view(client):
    url = reverse('log_in')
    response = client.get(url)
    assert response.status_code == 200
    # assert_status_codes(client, url, get=200)

@pytest.mark.django_db
def test_player_view(client):
    url = reverse('player', kwargs={'pk': 1})
    assert_status_codes(client, url, get=200)

def test_log_out_view(client):
    url = reverse('log_out')
    assert_status_codes(client, url, _all=302)

def test_upload_view(client):
    url = reverse('upload')
    assert_status_codes(client, url, _all=302)

def test_liked_view(client):
    url = reverse('liked')
    assert_status_codes(client, url, _all=302)

def test_follow_view(client):
    url = reverse('follow', kwargs={'username': 'test'})
    assert_status_codes(client, url, _all=302)

def test_following_view(client):
    url = reverse('following')
    assert_status_codes(client, url, _all=302)

def test_avatar_upload_view(client):
    url = reverse('avatar_upload')
    assert_status_codes(client, url, _all=302)

def test_delete_view(client):
    url = reverse('delete', kwargs={'pk': 1})
    assert_status_codes(client, url, _all=302)
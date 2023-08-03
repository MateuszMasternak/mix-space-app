import pytest

from django.urls import reverse


@pytest.fixture
def sample_user(django_user_model):
    username = 'TestUsername'
    email = 'testemail@example.com'
    password = 'TestPassword123!'
    return django_user_model.objects.create_user(username=username,
                                                 email=email,
                                                 password=password)

def test_upload_view(client, sample_user):
    client.force_login(sample_user)
    url = reverse('upload')
    response = client.get(url)
    assert response.status_code == 200

def test_liked_view(client, sample_user):
    client.force_login(sample_user)
    url = reverse('liked')
    response = client.get(url)
    assert response.status_code == 200

def test_follow_view(client, sample_user):
    client.force_login(sample_user)
    url = reverse('follow', kwargs={'username': 'test'})
    response = client.get(url)
    assert response.status_code == 404

def test_follow_view_with_second_user(client, sample_user, django_user_model):
    username = 'TestUsername2'
    email = 'testemail2@example.com'
    password = 'TestPassword123!'
    django_user_model.objects.create_user(username=username,
                                          email=email,
                                          password=password)
    client.force_login(sample_user)
    url = reverse('follow', kwargs={'username': 'TestUsername2'})
    response = client.get(url)
    assert response.status_code == 200

def test_following_view(client, sample_user):
    client.force_login(sample_user)
    url = reverse('following')
    response = client.get(url)
    assert response.status_code == 200

# def test_avatar_upload_view(client, sample_user):
#     client.force_login(sample_user)
#     url = reverse('avatar_upload')
#     response = client.get(url)
#     assert response.status_code == 302
#
# def test_delete_view(client, sample_user):
#     client.force_login(sample_user)
#     url = reverse('delete', kwargs={'pk': 1})
#     response = client.get(url)
#     assert response.status_code == 302

def test_log_out_view(client, sample_user):
    client.force_login(sample_user)
    url = reverse('log_out')
    response = client.get(url)
    assert response.status_code == 302
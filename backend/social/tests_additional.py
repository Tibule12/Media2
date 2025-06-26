import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Post

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def post(user):
    return Post.objects.create(author=user, content='Test post content')

@pytest.mark.django_db
def test_get_user_profile(authenticated_client, user):
    url = reverse('current-user-profile')
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert response.data['username'] == user.username
    assert 'photos_count' in response.data
    assert 'followers_count' in response.data
    assert 'follows_count' in response.data

@pytest.mark.django_db
def test_get_posts_list(authenticated_client, post):
    url = reverse('post-list')
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert any(p['id'] == post.id for p in response.data)

@pytest.mark.django_db
def test_create_post(authenticated_client):
    url = reverse('post-list')
    data = {'content': 'New post content'}
    response = authenticated_client.post(url, data)
    assert response.status_code == 201
    assert response.data['content'] == data['content']

import pytest

@pytest.mark.django_db
def test_unauthenticated_access(api_client):
    url = reverse('current-user-profile')
    response = api_client.get(url)
    assert response.status_code == 401

    url = reverse('post-list')
    response = api_client.get(url)
    assert response.status_code == 200  # Assuming posts list is public

@pytest.mark.django_db
def test_edge_case_empty_content(authenticated_client):
    url = reverse('post-list')
    data = {'content': ''}
    response = authenticated_client.post(url, data)
    assert response.status_code == 400  # Assuming empty content is invalid

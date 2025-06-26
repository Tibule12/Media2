import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Post, Story, Follow

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
    return user

@pytest.mark.django_db
def test_post_list(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    response = api_client.get('/api/posts/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_story_list(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    response = api_client.get('/api/stories/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_follow_list(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    response = api_client.get('/api/follows/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_list(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    response = api_client.get('/api/users/')
    assert response.status_code == 200

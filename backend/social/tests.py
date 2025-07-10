from django.urls import reverse
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch

class SocialAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_uid = 'testuid123'
        self.test_token = 'testtoken123'
        self.auth_header = f'Bearer {self.test_token}'

    @patch('social.authentication.SupabaseAuthentication.authenticate')
    def test_get_user_profile(self, mock_authenticate):
        mock_user = type('User', (), {
            'username': self.test_uid,
            'email': 'test@example.com',
            'display_name': 'Test User',
            'is_authenticated': True,
        })()
        mock_authenticate.return_value = (mock_user, None)

        url = reverse('get_user_profile')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['uid'], self.test_uid)
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['display_name'], 'Test User')

    def test_get_user_profile_unauthorized(self):
        url = reverse('get_user_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('social.authentication.SupabaseAuthentication.authenticate')
    def test_posts_get_and_post(self, mock_authenticate):
        mock_authenticate.return_value = (type('User', (), {'username': 'testuser', 'is_authenticated': True})(), None)
        url = reverse('posts')

        # Test GET posts
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test POST post
        data = {'content': 'Test post content', 'created_at': '2025-07-10T12:00:00Z'}
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], 'testuser')
        self.assertEqual(response.data['content'], 'Test post content')

    @patch('social.authentication.SupabaseAuthentication.authenticate')
    def test_notifications_list(self, mock_authenticate):
        mock_authenticate.return_value = (type('User', (), {'username': 'testuser', 'is_authenticated': True})(), None)
        url = reverse('list_notifications')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('social.authentication.SupabaseAuthentication.authenticate')
    def test_stories_list(self, mock_authenticate):
        mock_authenticate.return_value = (type('User', (), {'username': 'testuser', 'is_authenticated': True})(), None)
        url = reverse('list_stories')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('social.authentication.SupabaseAuthentication.authenticate')
    def test_search(self, mock_authenticate):
        mock_authenticate.return_value = (type('User', (), {'username': 'testuser', 'is_authenticated': True})(), None)
        url = reverse('search')
        response = self.client.get(url + '?q=test', HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    @patch('social.authentication.SupabaseAuthentication.authenticate')
    def test_chat_conversations_and_messages(self, mock_authenticate):
        mock_authenticate.return_value = (type('User', (), {'username': 'testuser', 'is_authenticated': True})(), None)
        url_conversations = reverse('chat_conversations')
        url_messages = reverse('conversation_messages', args=['1'])

        response = self.client.get(url_conversations, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url_messages, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

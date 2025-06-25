from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Story, Follow, Notification

class SocialMediaAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.client.force_authenticate(user=self.user1)

    def test_post_creation_and_list(self):
        response = self.client.post('/api/posts/', {'content': 'Test post content'})
        if response.status_code != 201:
            print('Post creation failed:', response.content)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)

    def test_like_unlike_post(self):
        post_response = self.client.post('/api/posts/', {'content': 'Like test post'})
        if post_response.status_code != 201:
            print('Post creation failed:', post_response.content)
        post_id = post_response.data['id']
        like_response = self.client.post(f'/api/posts/{post_id}/like/')
        self.assertEqual(like_response.data['status'], 'liked')
        unlike_response = self.client.post(f'/api/posts/{post_id}/like/')
        self.assertEqual(unlike_response.data['status'], 'unliked')

    def test_comment_creation_and_list(self):
        post_response = self.client.post('/api/posts/', {'content': 'Comment test post'})
        if post_response.status_code != 201:
            print('Post creation failed:', post_response.content)
        post_id = post_response.data['id']
        comment_response = self.client.post('/api/comments/', {'post': post_id, 'content': 'Test comment'})
        self.assertEqual(comment_response.status_code, 201)
        list_response = self.client.get('/api/comments/')
        self.assertEqual(list_response.status_code, 200)
        self.assertTrue(len(list_response.data) > 0)

    def test_follow_unfollow(self):
        follow_response = self.client.post('/api/follows/follow/', {'user_id': self.user2.id})
        self.assertEqual(follow_response.status_code, 201)
        unfollow_response = self.client.post('/api/follows/unfollow/', {'user_id': self.user2.id})
        self.assertEqual(unfollow_response.status_code, 204)

    def test_story_creation(self):
        # Story model requires 'media' and 'expires_at' fields
        from django.core.files.uploadedfile import SimpleUploadedFile
        from django.utils import timezone
        from datetime import timedelta
        media_file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        expires_at = (timezone.now() + timedelta(hours=24)).isoformat()
        story_response = self.client.post('/api/stories/', {'media': media_file, 'expires_at': expires_at})
        if story_response.status_code != 201:
            print('Story creation failed:', story_response.content)
        self.assertEqual(story_response.status_code, 201)

    def test_notifications_list(self):
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.client.get('/api/search/', {'q': 'user1'})
        self.assertEqual(response.status_code, 200)

    def test_register_and_login(self):
        self.client.logout()
        register_response = self.client.post('/api/auth/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass',
            'first_name': 'New',
            'last_name': 'User'
        })
        if register_response.status_code != 201:
            print('Register failed:', register_response.content)
        self.assertEqual(register_response.status_code, 201)
        login_response = self.client.post('/api/auth/login/', {
            'email': 'newuser@example.com',
            'password': 'newpass'
        })
        if login_response.status_code != 200:
            print('Login failed:', login_response.content)
        self.assertEqual(login_response.status_code, 200)
        self.assertIn('token', login_response.data)

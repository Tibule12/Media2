from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Post, Comment, Like

class SocialAppTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', password='pass1234')
        self.post1 = Post.objects.create(author=self.user1, content='Post 1 content')
        self.post2 = Post.objects.create(author=self.user2, content='Post 2 content')

    def test_post_list(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_post_create_authenticated(self):
        self.client.login(username='user1', password='pass1234')
        url = reverse('post-list')
        data = {'content': 'New post content'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)
        self.client.logout()

    def test_post_create_unauthenticated(self):
        url = reverse('post-list')
        data = {'content': 'New post content'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_like_unlike(self):
        self.client.login(username='user1', password='pass1234')
        url = reverse('post-like', args=[self.post2.id])
        # Like the post
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'liked')
        self.assertEqual(Like.objects.filter(post=self.post2, user=self.user1).count(), 1)
        # Unlike the post
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'unliked')
        self.assertEqual(Like.objects.filter(post=self.post2, user=self.user1).count(), 0)
        self.client.logout()

    def test_comment_create_authenticated(self):
        self.client.login(username='user2', password='pass1234')
        url = reverse('comment-list')
        data = {'post': str(self.post1.id), 'content': 'Nice post!'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.client.logout()

    def test_comment_create_unauthenticated(self):
        url = reverse('comment-list')
        data = {'post': self.post1.id, 'content': 'Nice post!'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_list(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

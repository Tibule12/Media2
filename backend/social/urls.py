from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, UserViewSet, SearchView, RegisterView, StoryViewSet, FollowViewSet, NotificationViewSet, ChatConversationsView, ChatMessagesView
from .views_user_profile import CurrentUserProfileView, FollowUserView, UnfollowUserView
from .views_login import LoginViewWithRememberMe
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'users', UserViewSet, basename='user')
router.register(r'stories', StoryViewSet, basename='story')
router.register(r'follows', FollowViewSet, basename='follow')
router.register(r'notifications', NotificationViewSet, basename='notification')

from .views import DeleteTestUserView

urlpatterns = [
    # Move 'users/me/' path before router.urls to avoid conflict with UserViewSet
    path('users/me/', CurrentUserProfileView.as_view(), name='current-user-profile'),
    path('users/<str:username>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('users/<str:username>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('', include(router.urls)),
    path('search/', SearchView.as_view(), name='search'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginViewWithRememberMe.as_view(), name='login'),
    path('auth/delete_test_user/', DeleteTestUserView.as_view(), name='delete-test-user'),
    path('chat/conversations/', ChatConversationsView.as_view(), name='chat-conversations'),
    path('chat/conversations/<int:participant_id>/messages/', ChatMessagesView.as_view(), name='chat-messages'),
]

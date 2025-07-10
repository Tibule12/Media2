from django.urls import path
from . import views
from . import views_auth
from . import views_posts
from . import views_notifications
from . import views_stories
from . import views_search
from . import views_chat

urlpatterns = [
    path('users/me/', views.get_user_profile, name='get_user_profile'),
    path('chat/conversations/', views_chat.chat_conversations, name='chat_conversations'),
    path('chat/conversations/<str:conversation_id>/messages/', views_chat.conversation_messages, name='conversation_messages'),
    path('auth/register/', views_auth.register, name='register'),
    path('auth/login/', views_auth.login, name='login'),
    path('posts/', views_posts.posts, name='posts'),
    path('notifications/', views_notifications.list_notifications, name='list_notifications'),
    path('stories/', views_stories.list_stories, name='list_stories'),
    path('search/', views_search.search, name='search'),
]

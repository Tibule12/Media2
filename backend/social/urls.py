from django.urls import path
from . import views
from . import views_auth

urlpatterns = [
    path('users/me/', views.get_user_profile, name='get_user_profile'),
    # Commenting out chat related paths as views are missing
    # path('chat/conversations/', views.chat_conversations, name='chat_conversations'),
    # path('chat/conversations/<str:conversation_id>/messages/', views.conversation_messages, name='conversation_messages'),
    path('auth/register/', views_auth.register, name='register'),
    path('auth/login/', views_auth.login, name='login'),
]

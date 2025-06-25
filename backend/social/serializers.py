from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Media, Comment, Like, Story, Follow, Notification, Message

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']

from .models_user_profile import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['fullName', 'bio', 'profilePicture']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        fullName = profile_data.get('fullName')
        bio = profile_data.get('bio')
        profilePicture = profile_data.get('profilePicture')

        instance = super().update(instance, validated_data)

        profile = instance.profile
        if fullName is not None:
            profile.fullName = fullName
        if bio is not None:
            profile.bio = bio
        if profilePicture is not None:
            profile.profilePicture = profilePicture
        profile.save()

        return instance

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'file', 'media_type', 'uploaded_at']

class PostSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    likes = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'media', 'likes', 'comments']

    def get_likes(self, obj):
        return LikeSerializer(obj.likes.all(), many=True).data

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']

class StorySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Story
        fields = ['id', 'author', 'media', 'created_at', 'expires_at']

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField()
    following = serializers.StringRelatedField()

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.StringRelatedField()
    actor = serializers.StringRelatedField()
    target_post = PostSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target_post', 'timestamp', 'read']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    recipient = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp', 'read']

class ConversationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    participantName = serializers.CharField(read_only=True)

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content']

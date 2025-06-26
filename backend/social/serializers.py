from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Media, Comment, Like, Story, Follow, Notification, Message
from .models_user_profile import UserProfile

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']

class UserProfileSerializer(serializers.ModelSerializer):
    profilePicture = serializers.ImageField(use_url=True, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ['fullName', 'bio', 'profilePicture']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    photos_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    follows_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile', 'photos_count', 'followers_count', 'follows_count']

    def get_photos_count(self, obj):
        return obj.posts.count()

    def get_followers_count(self, obj):
        from .models import Follow
        return Follow.objects.filter(following=obj).count()

    def get_follows_count(self, obj):
        from .models import Follow
        return Follow.objects.filter(follower=obj).count()

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

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    birthday = serializers.DateField(required=False, allow_null=True)
    fullName = serializers.CharField(required=False, allow_blank=True)
    profilePicture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'birthday', 'fullName', 'profilePicture')

    def create(self, validated_data):
        birthday = validated_data.pop('birthday', None)
        fullName = validated_data.pop('fullName', '')
        profilePicture = validated_data.pop('profilePicture', None)
        email = validated_data['email']
        # Check if user with this email already exists
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists.")
        user = User.objects.create_user(
            username=email,  # Use email as username
            email=email,
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        # Create or update UserProfile
        profile = user.profile
        if fullName:
            profile.fullName = fullName
        if profilePicture:
            profile.profilePicture = profilePicture
        profile.save()
        # Birthday field is not in default User model; handle accordingly if you have a profile model
        # For now, ignoring birthday or you can extend User model to save it
        return user

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
    media = serializers.ImageField(use_url=True)

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

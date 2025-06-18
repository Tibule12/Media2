from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Story, Follow, Notification
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, UserSerializer, StorySerializer, FollowSerializer, NotificationSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .authentication import CsrfExemptSessionAuthentication
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication, CsrfExemptSessionAuthentication]

    def perform_create(self, serializer):
        user = self.request.user
        print(f"Authenticated user: {user}, is_authenticated: {user.is_authenticated}")
        post = serializer.save(author=user)
        # Save uploaded media files
        request = self.request
        for key, file in request.FILES.items():
            if key.startswith('media_'):
                # Determine media_type based on file content type or extension
                content_type = file.content_type
                if content_type.startswith('image/'):
                    media_type = 'image'
                elif content_type.startswith('video/'):
                    media_type = 'video'
                else:
                    media_type = 'other'
                post.media.create(file=file, media_type=media_type)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like, created = Like.objects.get_or_create(post=post, user=user)
        if not created:
            like.delete()
            return Response({'status': 'unliked'})
        return Response({'status': 'liked'})

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [CsrfExemptSessionAuthentication, TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by('-created_at')
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication, CsrfExemptSessionAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all().order_by('-created_at')
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, CsrfExemptSessionAuthentication]

    def create(self, request, *args, **kwargs):
        follower = request.user
        following_id = request.data.get('following')
        if not following_id:
            return Response({'error': 'Following user ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        if int(following_id) == follower.id:
            return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(follower=follower, following_id=following_id).exists():
            return Response({'error': 'Already following this user'}, status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.create(follower=follower, following_id=following_id)
        serializer = self.get_serializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        follower = request.user
        follow_id = kwargs.get('pk')
        try:
            follow = Follow.objects.get(id=follow_id, follower=follower)
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            return Response({'error': 'Follow relationship not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def follow(self, request):
        follower = request.user
        following_id = request.data.get('user_id')
        if not following_id:
            return Response({'error': 'User ID to follow is required'}, status=status.HTTP_400_BAD_REQUEST)
        if int(following_id) == follower.id:
            return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(follower=follower, following_id=following_id).exists():
            return Response({'error': 'Already following this user'}, status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.create(follower=follower, following_id=following_id)
        serializer = self.get_serializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def unfollow(self, request):
        follower = request.user
        following_id = request.data.get('user_id')
        if not following_id:
            return Response({'error': 'User ID to unfollow is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            follow = Follow.objects.get(follower=follower, following_id=following_id)
            follow.delete()
            return Response({'status': 'unfollowed'}, status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            return Response({'error': 'Follow relationship not found'}, status=status.HTTP_404_NOT_FOUND)

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(recipient=user).order_by('-created_at')

class SearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        query = request.query_params.get('q', '')
        if not query:
            return Response([], status=status.HTTP_200_OK)

        users = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
        posts = Post.objects.filter(content__icontains=query)

        user_serializer = UserSerializer(users, many=True)
        post_serializer = PostSerializer(posts, many=True)

        results = []

        for user in user_serializer.data:
            results.append({
                'type': 'user',
                'id': user['id'],
                'username': user['username'],
                'first_name': user.get('first_name', ''),
                'last_name': user.get('last_name', ''),
            })

        for post in post_serializer.data:
            results.append({
                'type': 'post',
                'id': post['id'],
                'title': post.get('content', '')[:50],  # Use first 50 chars as title
            })

        return Response(results, status=status.HTTP_200_OK)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    birthday = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'birthday')

    def create(self, validated_data):
        birthday = validated_data.pop('birthday', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        # Birthday field is not in default User model; handle accordingly if you have a profile model
        # For now, ignoring birthday or you can extend User model to save it
        return user

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        # Log errors for debugging
        print("Registration errors:", serializer.errors)
        # Return detailed errors for debugging
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

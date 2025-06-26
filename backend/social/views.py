from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, serializers, viewsets
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Story, Follow, Notification, Message
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, UserSerializer, StorySerializer, FollowSerializer, NotificationSerializer, MessageSerializer, ConversationSerializer, MessageCreateSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .authentication import CsrfExemptSessionAuthentication
from rest_framework.decorators import action
from django.db.models import Q
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
                # Provide a default media_type value to satisfy NOT NULL constraint
                post.media.create(file=file, media_type='unknown')

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

class DeleteTestUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def delete(self, request):
        try:
            user = User.objects.get(username='testuser')
            user.delete()
            return Response({'message': 'Test user deleted successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'Test user does not exist'}, status=status.HTTP_404_NOT_FOUND)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    birthday = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'birthday')

    def create(self, validated_data):
        birthday = validated_data.pop('birthday', None)
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

    def put(self, request):
        # Support for multipart/form-data for profile picture upload
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = None
        if email:
            from django.contrib.auth import get_user_model
            UserModel = get_user_model()
            try:
                user_obj = UserModel.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
            except UserModel.DoesNotExist:
                user = None
            except UserModel.MultipleObjectsReturned:
                # Handle multiple users with same email gracefully
                user = UserModel.objects.filter(email=email).first()
                user = authenticate(username=user.username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by('-created_at')
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication, CsrfExemptSessionAuthentication]

    def perform_create(self, serializer):
        user = self.request.user
        story = serializer.save(author=user)
        # Additional logic for story creation can be added here

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all().order_by('-created_at')
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication, CsrfExemptSessionAuthentication]

    def perform_create(self, serializer):
        user = self.request.user
        follow = serializer.save(follower=user)
        # Additional logic for follow creation can be added here

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication, CsrfExemptSessionAuthentication]

    def perform_create(self, serializer):
        user = self.request.user
        notification = serializer.save()
        # Additional logic for notification creation can be added here

class ChatConversationsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        # Placeholder implementation for chat conversations list
        return Response({"message": "List of chat conversations"}, status=200)

class ChatMessagesView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, participant_id):
        # Placeholder implementation for chat messages with a participant
        return Response({"message": f"Messages with participant {participant_id}"}, status=200)

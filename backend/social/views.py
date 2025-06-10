from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
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
    authentication_classes = [SessionAuthentication, BasicAuthentication]

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

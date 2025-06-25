from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from .models import Follow

from rest_framework.authentication import TokenAuthentication
from .authentication import CsrfExemptSessionAuthentication

class CurrentUserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, CsrfExemptSessionAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        import logging
        logger = logging.getLogger(__name__)
        user = request.user
        data = request.data.copy()
        # Handle nested profile data
        profile_data = {}
        for key in ['fullName', 'bio', 'profilePicture']:
            if key in data:
                profile_data[key] = data.pop(key)
        if profile_data:
            data['profile'] = profile_data

        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            logger.error(f"User profile update errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        follower = request.user
        following = get_object_or_404(User, username=username)
        if follower == following:
            return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(follower=follower, following=following).exists():
            return Response({'error': 'Already following this user'}, status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.create(follower=follower, following=following)
        return Response({'status': 'followed'}, status=status.HTTP_201_CREATED)

class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        follower = request.user
        following = get_object_or_404(User, username=username)
        try:
            follow = Follow.objects.get(follower=follower, following=following)
            follow.delete()
            return Response({'status': 'unfollowed'}, status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            return Response({'error': 'Follow relationship not found'}, status=status.HTTP_404_NOT_FOUND)

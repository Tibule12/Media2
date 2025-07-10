from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

# Dummy in-memory posts storage for demonstration
posts_data = []

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def posts(request):
    if request.method == 'GET':
        sort = request.query_params.get('sort')
        sorted_posts = posts_data
        if sort == 'newest':
            sorted_posts = sorted(posts_data, key=lambda x: x.get('created_at', ''), reverse=True)
        return Response(sorted_posts)
    elif request.method == 'POST':
        data = request.data
        post = {
            'id': len(posts_data) + 1,
            'author': request.user.username,
            'content': data.get('content', ''),
            'created_at': data.get('created_at', ''),
        }
        posts_data.append(post)
        return Response(post, status=status.HTTP_201_CREATED)

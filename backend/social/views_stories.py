from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Dummy in-memory stories storage for demonstration
stories = []

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_stories(request):
    user = request.user.username
    user_stories = [s for s in stories if s.get('author') == user]
    return Response(user_stories)

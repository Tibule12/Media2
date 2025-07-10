from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Dummy in-memory notifications storage for demonstration
notifications = []

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_notifications(request):
    user = request.user.username
    user_notifications = [n for n in notifications if n.get('recipient') == user]
    return Response(user_notifications)

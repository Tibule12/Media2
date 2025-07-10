from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Dummy in-memory chat storage for demonstration
conversations = []
messages = []

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_conversations(request):
    user = request.user.username
    user_conversations = [c for c in conversations if user in c.get('participants', [])]
    return Response(user_conversations)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversation_messages(request, conversation_id):
    conv_messages = [m for m in messages if m.get('conversation_id') == conversation_id]
    return Response(conv_messages)

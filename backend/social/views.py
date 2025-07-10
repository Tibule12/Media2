from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . import firebase_client  # Ensure Firebase Admin SDK is initialized
from rest_framework.views import exception_handler

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    try:
        user = request.user
        user_data = {
            'uid': user.username,
            'email': getattr(user, 'email', ''),
            'display_name': getattr(user, 'display_name', ''),
            # Add any additional registration details here if stored in backend database
        }
        return Response(user_data)
    except Exception as e:
        response = exception_handler(e, context=None)
        if response is None:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response

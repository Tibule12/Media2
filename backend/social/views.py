from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from firebase_admin import auth
from rest_framework.views import exception_handler

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_profile(request):
    try:
        id_token = request.headers.get('Authorization')
        if not id_token:
            return Response({'error': 'Authorization header missing'}, status=status.HTTP_401_UNAUTHORIZED)
        # Remove 'Bearer ' prefix if present
        if id_token.startswith('Bearer '):
            id_token = id_token[7:]
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token.get('uid')
        if not uid:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        user = auth.get_user(uid)
        user_data = {
            'uid': user.uid,
            'email': user.email,
            'display_name': user.display_name,
        }
        return Response(user_data)
    except Exception as e:
        response = exception_handler(e, context=None)
        if response is None:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response

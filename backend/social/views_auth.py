from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from firebase_admin import auth
from rest_framework.views import exception_handler

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    try:
        data = request.data
        email = data.get('email')
        password = data.get('password')
        display_name = data.get('fullName') or data.get('username')

        if not email or not password or not display_name:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )

        # Optionally, store additional user info in Firestore here

        return Response({'message': 'User registered successfully', 'uid': user.uid}, status=status.HTTP_201_CREATED)
    except Exception as e:
        response = exception_handler(e, context=None)
        if response is None:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from firebase_admin import auth
from rest_framework.views import exception_handler

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        data = request.data
        email = data.get('email')
        password = data.get('password')
        id_token = data.get('idToken')

        if not id_token:
            return Response({'error': 'Missing idToken'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token.get('uid')

        if not uid:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        # Optionally, fetch user info from Firebase
        user = auth.get_user(uid)

        return Response({'message': 'Login successful', 'uid': uid, 'email': user.email, 'displayName': user.display_name}, status=status.HTTP_200_OK)
    except Exception as e:
        response = exception_handler(e, context=None)
        if response is None:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response

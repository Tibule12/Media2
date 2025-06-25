from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models_login_history import LoginHistory
from django.utils.timezone import now
from datetime import timedelta

class LoginViewWithRememberMe(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        import logging
        logger = logging.getLogger(__name__)
        email = request.data.get('email')
        password = request.data.get('password')
        remember_me = request.data.get('remember_me', False)
        if email:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user_objs = User.objects.filter(email=email)
                if user_objs.count() == 1:
                    user_obj = user_objs.first()
                    user = authenticate(username=user_obj.username, password=password)
                else:
                    user = None
            except User.DoesNotExist:
                user = None
        else:
            user = None
        if user:
            token, created = Token.objects.get_or_create(user=user)
            # Optionally extend token expiration or handle remember_me logic here
            # For simplicity, token is permanent; implement expiration if needed

            # Log login history
            ip = request.META.get('REMOTE_ADDR')
            if ip is None:
                ip = '0.0.0.0'
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            try:
                LoginHistory.objects.create(user=user, ip_address=ip, user_agent=user_agent)
            except Exception as e:
                logger.error(f"Failed to log login history: {e}")

            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            logger.warning(f"Failed login attempt for email: {email}")
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

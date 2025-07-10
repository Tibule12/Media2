from rest_framework import authentication, exceptions
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
import logging
import jwt
import requests

User = get_user_model()
logger = logging.getLogger(__name__)

class SupabaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            logger.warning('Authorization header missing')
            return None
        if not auth_header.startswith('Bearer '):
            logger.warning('Authorization header does not start with Bearer')
            return None
        token = auth_header.split('Bearer ')[1]
        try:
            # Fetch Supabase public keys for JWT verification
            jwks_url = 'https://mszactexqxdjnyarbesw.supabase.co/auth/v1/certs'
            jwks = requests.get(jwks_url).json()
            # Decode and verify JWT token
            decoded_token = jwt.decode(token, jwks, algorithms=['RS256'], audience='mszactexqxdjnyarbesw', options={"verify_exp": True})
            uid = decoded_token.get('sub')
            if not uid:
                logger.error('Invalid Supabase JWT token: no sub')
                raise exceptions.AuthenticationFailed('Invalid Supabase JWT token')
            user, created = User.objects.get_or_create(username=uid)
            logger.info(f'Authenticated user {uid}, created={created}')
            return (user, None)
        except Exception as e:
            logger.error(f'Supabase authentication failed: {str(e)}')
            raise exceptions.AuthenticationFailed('Supabase authentication failed: ' + str(e))

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from firebase_admin import auth
from django.contrib.auth import get_user_model

User = get_user_model()


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            decoded_token = auth.verify_id_token(token)
        except Exception:
            raise AuthenticationFailed('Token de Firebase inválido o expirado.')

        email = decoded_token.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed('Usuario no encontrado.')

        return (user, None)

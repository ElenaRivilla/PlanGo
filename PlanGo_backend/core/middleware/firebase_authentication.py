from django.utils.deprecation import MiddlewareMixin
from config.firebase_config import auth
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

class FirebaseAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Permitir solicitudes OPTIONS
        if request.method == 'OPTIONS':
            return None

        # Excluir rutas públicas
        public_paths = [
            '/users/login-with-google',
            '/users/register',
            '/admin',
            '/itineraries/geocodenames'
        ]

        # Normaliza la ruta (quita slash final para comparar)
        path = request.path.rstrip('/')
        # Revisar y registrar si es ruta pública
        for p in public_paths:
            p_norm = p.rstrip('/')
            if path == p_norm or path.startswith(p_norm + '/'):
                print("Public path accessed:", request.path)
                return None

        # Obtener el token del encabezado Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Token no proporcionado'}, status=401)

        token = auth_header.split(' ')[1]

        try:
            # Verificar el token de Firebase
            decoded_token = auth.verify_id_token(token)
            email = decoded_token.get('email')
            name = decoded_token.get('name', '')
            picture = decoded_token.get('picture', '')

            # Buscar o crear el usuario en la base de datos
            user, created = User.objects.get_or_create(email=email, defaults={
                'first_name': name.split()[0] if name else '',
                'last_name': name.split()[1] if len(name.split()) > 1 else '',
                'user_image': picture,
            })

            # Asignar el usuario autenticado al objeto request
            request.user = user

        except Exception as e:
            return JsonResponse({'error': 'Token inválido o expirado', 'detail': str(e)}, status=401)
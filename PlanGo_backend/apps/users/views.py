from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from apps.users.models.user import User
from apps.users.models.participant import Participant
from .serializer import ParticipantSerializer
import json
from firebase_admin import auth
from config.firebase_config import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from apps.users.service import split_full_name
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# USERS
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        try:
            # Verificar el encabezado de autorización
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse({'error': 'Token no proporcionado'}, status=401)

            token = auth_header.split(' ')[1]

            # Verificar el token de Firebase
            try:
                decoded_token = auth.verify_id_token(token)
                uid = decoded_token['uid']
            except Exception as e:
                return JsonResponse({'error': 'Token inválido o expirado'}, status=401)

            # Procesar los datos del cuerpo de la solicitud
            body = json.loads(request.body)
            payload = body.get('payload', {})  # Obtén el objeto 'payload'

            email = payload.get('email')
            first_name = payload.get('first_name')
            last_name = payload.get('last_name')
            username = payload.get('username')
            firebase_uid = payload.get('firebase_uid')
            
            # Validar que los campos requeridos estén presentes
            if not email or not first_name or not last_name or not username or not firebase_uid:
                return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400)

            # Crear un nuevo usuario en la base de datos de Django
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'firebase_uid': firebase_uid,
                    'username': username,
                }
            )

            if not created:
                return JsonResponse({'error': 'El usuario ya existe'}, status=400)

            return JsonResponse({'message': 'Usuario registrado exitosamente'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
       
        
@method_decorator(csrf_exempt, name='dispatch')
class LoginWithGoogleView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Obtén el token del encabezado Authorization
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse({'error': 'Token no proporcionado'}, status=401)

            token = auth_header.split(' ')[1]

            # Verifica el token de Firebase
            try:
                decoded_token = auth.verify_id_token(token)
                uid = decoded_token['uid']
            except Exception as e:
                return JsonResponse({'error': 'Token inválido o expirado'}, status=401)

            # Si faltan nombre o apellidos, extraerlos desde Firebase
            firebase_user = auth.get_user(uid)
            full_name = firebase_user.display_name or ""
            profile_image = firebase_user.photo_url
            first_name, last_name = split_full_name(full_name)
            username = f"{first_name[0]}{last_name.split(" ")[0]}".lower()
            email = decoded_token['email']
            
            # Busca o crea el usuario en la base de datos de Django
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'firebase_uid': uid,
                    'user_image': profile_image,
                    'username': username
                }
            )

            return JsonResponse({'message': 'Usuario autenticado exitosamente'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
       
@method_decorator(csrf_exempt, name='dispatch')
class LoginWithEmailView(View):
    def post(self, request):
        try:
            # Procesar los datos del cuerpo de la solicitud
            body = json.loads(request.body)
            id_token = body.get('idToken')

            # Validar que el token esté presente
            if not id_token:
                return JsonResponse({'error': 'Token no proporcionado'}, status=400)

            # Verificar el token de Firebase
            try:
                decoded_token = auth.verify_id_token(id_token)
                uid = decoded_token.get('uid')

                # Usuario autenticado correctamente
                return JsonResponse({'message': 'Inicio de sesión exitoso'}, status=200)
            except Exception as e:
                return JsonResponse({'error': 'Token inválido o expirado'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
@csrf_exempt
def get_userId_by_userUid(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uid = data.get('uid')
        try:
            user = User.objects.get(firebase_uid=uid)
            return JsonResponse({'id': user.id})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


# PARTICIPANTS
@csrf_exempt
def get_participants_by_destination(request, destination_id):
    participants = Participant.objects.filter(destination=destination_id)
    if not participants.exists():
        return JsonResponse({'error': 'No hay destinos creados con este usuario.'}, status=404)

    data = [
        {
            'participant_id': p.participant_id,
            'destination_id': p.destination.id,
            'user': p.user.id if p.user else None,
            'participant_name': p.participant_name,
            'is_user': False
        }
        for p in participants
    ]

    user = request.user
    if user.is_authenticated:
        data.insert(0, {
            'participant_id': None,
            'destination_id': destination_id,
            'user': user.id,
            'participant_name': user.username,
            'is_user': True
        })
    return JsonResponse({'Participants': data})
    
    
@csrf_exempt
def create_participant(request):
    if request.method == 'POST':
            try:
                data = json.loads(request.body)
                serializer = ParticipantSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status=201)
                return JsonResponse({'error': serializer.errors}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        return JsonResponse({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_image': user.user_image,
            # ...otros campos que quieras exponer
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)


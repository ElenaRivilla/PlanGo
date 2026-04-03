from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import get_object_or_404
from apps.users.models.user import User
from apps.users.models.participant import Participant
from .serializer import ParticipantSerializer
import json
from firebase_admin import auth
from config.firebase_config import *
from apps.users.service import split_full_name
from apps.users.DTO.users_dto import map_user, map_participant
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


# USERS
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse({'error': 'Token no proporcionado'}, status=401)

            token = auth_header.split(' ')[1]

            try:
                decoded_token = auth.verify_id_token(token)
                uid = decoded_token['uid']
            except Exception:
                return JsonResponse({'error': 'Token inválido o expirado'}, status=401)

            body = json.loads(request.body)
            payload = body.get('payload', {})

            email = payload.get('email')
            first_name = payload.get('first_name')
            last_name = payload.get('last_name')
            username = payload.get('username')
            firebase_uid = payload.get('firebase_uid')

            if not all([email, first_name, last_name, username, firebase_uid]):
                return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400)

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
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse({'error': 'Token no proporcionado'}, status=401)

            token = auth_header.split(' ')[1]

            try:
                decoded_token = auth.verify_id_token(token)
                uid = decoded_token['uid']
            except Exception:
                return JsonResponse({'error': 'Token inválido o expirado'}, status=401)

            firebase_user = auth.get_user(uid)
            full_name = firebase_user.display_name or ""
            profile_image = firebase_user.photo_url
            first_name, last_name = split_full_name(full_name)
            username = f"{first_name[0]}{last_name.split(' ')[0]}".lower()
            email = decoded_token['email']

            User.objects.get_or_create(
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
            body = json.loads(request.body)
            id_token = body.get('idToken')

            if not id_token:
                return JsonResponse({'error': 'Token no proporcionado'}, status=400)

            try:
                auth.verify_id_token(id_token)
                return JsonResponse({'message': 'Inicio de sesión exitoso'}, status=200)
            except Exception:
                return JsonResponse({'error': 'Token inválido o expirado'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_userId_by_userUid(request):
    uid = request.data.get('uid')
    user = get_object_or_404(User, firebase_uid=uid)
    return JsonResponse({'id': user.id})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return JsonResponse(map_user(user))


# PARTICIPANTS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_participants_by_destination(request, destination_id):
    participants = Participant.objects.filter(destination=destination_id)
    if not participants.exists():
        return JsonResponse({'error': 'No hay participantes en este destino.'}, status=404)

    data = [map_participant(p) for p in participants]

    user = request.user
    user_entry = {
        'participant_id': None,
        'destination_id': destination_id,
        'user': user.id,
        'participant_name': user.username,
        'is_user': True,
    }
    return JsonResponse({'Participants': [user_entry] + data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_participant(request):
    serializer = ParticipantSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse({'error': serializer.errors}, status=400)

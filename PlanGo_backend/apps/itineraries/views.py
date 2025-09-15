from django.shortcuts import render
from django.http import JsonResponse
from .serializer import ItinerarySerializer, DestinationSerializer, FormItinerarySerializer
from apps.itineraries.models.itinerary import Itinerary
from apps.itineraries.models.destination import Destination
from apps.places.models.accommodation import Accommodation
from apps.places.models.activity import Activity
from apps.places.models.restaurant import Restaurant
from apps.expenses.models.expense import Expense
from apps.users.models.user import User
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from django.utils import timezone
from django.views import View
from django.db.models import Sum
from django.db import models
import pycountry
import requests
import json
from datetime import timedelta

# Create your views here.
GEONAMES_API_KEY = settings.GEONAMES_API_KEY  

def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrftoken': token})  

# ITINERARIOS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_itineraries(request):
    itineraries = Itinerary.objects.all()
    if not itineraries.exists():
        return JsonResponse({'error': 'No hay itinerarios creados'}, status=404)
    data = [
        {
            'itinerary_id': i.itinerary_id,
            'itinerary_name': i.itinerary_name,
            'creator_user': i.creator_user.id if hasattr(i.creator_user, 'id') else i.creator_user,
            'creation_date': i.creation_date,
            'start_date': i.start_date,
            'end_date': i.end_date,
            'destinations_count': i.destinations.count(),
        }
        for i in itineraries
    ]
    return JsonResponse({'itineraries': data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])   
def get_itineraries_by_user(request, user_id):
    itineraries = Itinerary.objects.filter(creator_user=user_id)
    if not itineraries.exists():
        return JsonResponse({'error': 'No hay itinerarios creados con este usuario.'}, status=404)
    data = []
    for i in itineraries:
        countries = i.countries.split(',') if i.countries else []
        countries_count = len(countries)
        destinations_count = Destination.objects.filter(itinerary=i).count()
        data.append({
            'itinerary_id': i.itinerary_id,
            'itinerary_name': i.itinerary_name,
            'creator_user': i.creator_user.id if hasattr(i.creator_user, 'id') else i.creator_user,
            'creation_date': i.creation_date,
            'start_date': i.start_date,
            'end_date': i.end_date,
            'countries': countries,
            'destinations_count': destinations_count,
        })
    return JsonResponse({'itineraries': data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_itinerary_by_id(request, itinerary_id):
    try:
        itinerary = Itinerary.objects.get(pk=itinerary_id, creator_user=request.user)
        serializer = ItinerarySerializer(itinerary)
        return JsonResponse(serializer.data, safe=False)
    except Itinerary.DoesNotExist:
        return JsonResponse({'error': 'Itinerario no encontrado o no tienes permiso para acceder a él.'}, status=404)
# PlanGo_backend/apps/itineraries/views.py

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_countries_by_itinerary(request, itinerary_id):
    try:
        itinerary = Itinerary.objects.get(pk=itinerary_id)
        countries_str = itinerary.countries or ''
        countries_list = [c.strip() for c in countries_str.split(',') if c.strip()]
        return Response({'countries': countries_list})
    except Itinerary.DoesNotExist:
        return Response({'error': 'Itinerario no encontrado'}, status=404)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def create_itinerary(request):
    serializer = FormItinerarySerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# DESTINOS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_destinations(request):
    destination = Destination.objects.all()
    if not destination.exists():
        return JsonResponse({'error': 'No hay destinos creados'}, status=404)
    data = [
        {
            'destination_id': i.id,
            'itinerary_id': i.itinerary.itinerary_id if hasattr(i.itinerary, 'itinerary_id') else i.itinerary,            
            'country': i.country,
            'city_name': i.city_name,
            'start_date': i.start_date,
            'end_date': i.end_date,
            'latitude': i.latitude,
            'longitude': i.longitude,
        }
        for i in destination
    ]
    return JsonResponse({'destination': data})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def get_destinations_by_itinerary(request, itinerary_id):
    destination = Destination.objects.filter(itinerary=itinerary_id)
    if not destination.exists():
        return JsonResponse({'error': 'No hay destinos creados con este usuario.'}, status=404)
    data = [
        {
            'destination_id': i.id,
            'itinerary_id': i.itinerary.itinerary_id if hasattr(i.itinerary, 'itinerary_id') else i.itinerary,            
            'country': i.country,
            'city_name': i.city_name,
            'start_date': i.start_date,
            'end_date': i.end_date,
            'latitude': i.latitude,
            'longitude': i.longitude,
        }
        for i in destination

    ]
    return JsonResponse({'User destinations': data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_destination(request):
    data = request.data
    itinerary_id = data.get('itinerary')
    country = data.get('country')
    city_name = data.get('city_name')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    try:
        itinerary = Itinerary.objects.get(pk=itinerary_id)
    except Itinerary.DoesNotExist:
        return JsonResponse({'error': f'Itinerario con id {itinerary_id} no existe.'}, status=404)        
    destinos = Destination.objects.filter(itinerary=itinerary).order_by('-end_date')
    if destinos.exists():
        last_end_date = destinos.last().end_date
        start_date = last_end_date + timedelta(days=1)
    else:
        start_date = itinerary.start_date
    end_date = start_date   
    destination = Destination.objects.create(   
        itinerary=itinerary,
        country=country,
        city_name=city_name,
        start_date=start_date,
        end_date=end_date,
        latitude=latitude,
        longitude=longitude,
    )

    return JsonResponse({'status': 'ok', 'destination_id': destination.pk})
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_destination(request, destination_id):
    try:
        destination = Destination.objects.get(pk=destination_id)
    except Destination.DoesNotExist:
        return Response({'error': 'Destino no encontrado'}, status=status.HTTP_404_NOT_FOUND)
                                                                    # Actualizar un dato parcialmente (fechas del destino)
    serializer = DestinationSerializer(destination, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def destination_summary(request, destination_id):
    accommodations_count = Accommodation.objects.filter(destination_id=destination_id).count()
    activities_count = Activity.objects.filter(destination_id=destination_id).count()
    restaurants_count = Restaurant.objects.filter(destination_id=destination_id).count()
    expenses = Expense.objects.filter(destination_id=destination_id)
    total_expenses = expenses.aggregate(total=models.Sum('total_amount'))['total'] or 0

    return JsonResponse({
        'accommodations_count': accommodations_count,
        'activities_count': activities_count,
        'restaurants_count': restaurants_count,
        'total_expenses': float(total_expenses),
    })
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_countries_by_destination(request, destination_id):
    try:
        destination = Destination.objects.get(pk=destination_id)
        itinerary = destination.itinerary
        countries_str = itinerary.countries or ''
        countries_list = [c.strip() for c in countries_str.split(',') if c.strip()]
        return Response({'countries': countries_list, 'itinerary_id': itinerary.itinerary_id})
    except Destination.DoesNotExist:
        return Response({'error': 'Destino no encontrado'}, status=404)


def country_name_to_code(name):
    try:
        country = pycountry.countries.search_fuzzy(name)[0]
        return country.alpha_2
    except LookupError:
        return None
    
def country_names_to_codes(names):
    return [country_name_to_code(name) for name in names if country_name_to_code(name)]

# google_places_autocomplete
@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def geocodenames_autocomplete(request):
    input_text = request.GET.get('input')
    country_code = request.GET.get('country')
    api_key = GEONAMES_API_KEY 

    if not input_text or not country_code:
        return JsonResponse({'error': 'Missing input or country'}, status=400)

    # Endpoint actualizado para Places API (New)
    url = (
        f'http://api.geonames.org/searchJSON'
        f'?name_startsWith={input_text}&country={country_code}&featureClass=P&minPopulation=5000&maxRows=1000&username={api_key}&lang=es'
    )
    response = requests.get(url)
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to serch in GeoNames API'}, status=response.status_code)

    return JsonResponse(response.json())
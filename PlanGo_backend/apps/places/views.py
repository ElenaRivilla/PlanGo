from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
from apps.places.models.accommodation import Accommodation
from apps.users.models.user import User
from .serializer import AcommodationSerializer, ActivitySerializer, RestaurantSerializer, SavedPlacesSerializer
from ..itineraries.serializer import DestinationSerializer
from apps.places.models.accommodation_image import AccommodationImage
from apps.places.models.activity import Activity
from apps.places.models.activity_image import ActivityImage
from apps.itineraries.models.destination import Destination
from apps.places.models.restaurant import Restaurant
from apps.places.models.restaurant_image import RestaurantImage
from apps.places.models.saved_place import SavedPlace
from apps.places.models.saved_place_image import SavedPlaceImage
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings
import requests
import json
import os
# Create your views here.
PLACES_API_KEY = settings.API_KEY

# GENERAL DATA

accommodation_types = [
    'lodging', 'hotel', 'motel', 'resort_hotel', 'hostel', 'bed_and_breakfast',
    'guest_house', 'campground', 'mobile_home_park', 'cottage', 'extended_stay_hotel',
    'farmstay', 'budget_japanese_inn', 'japanese_inn', 'inn', 'private_guest_room', 'rv_park'
]

restaurant_types = [
    'restaurant', 'bar', 'cafe', 'bakery', 'bagel_shop', 'bar_and_grill', 'barbecue_restaurant',
    'buffet_restaurant', 'brunch_restaurant', 'breakfast_restaurant', 'hamburger_restaurant',
    'pub', 'fine_dining_restaurant', 'fast_food_restaurant', 'food_court', 'meal_takeaway',
    'meal_delivery', 'deli', 'confectionery', 'candy_store', 'chocolate_shop', 'chocolate_factory',
    'ice_cream_shop', 'dessert_shop', 'dessert_restaurant', 'donut_shop', 'cafeteria', 'coffee_shop',
    'juice_shop', 'wine_bar', 'sushi_restaurant', 'pizza_restaurant', 'mexican_restaurant',
    'italian_restaurant', 'indian_restaurant', 'chinese_restaurant', 'japanese_restaurant',
    'korean_restaurant', 'thai_restaurant', 'greek_restaurant', 'french_restaurant',
    'spanish_restaurant', 'american_restaurant', 'asian_restaurant', 'african_restaurant',
    'brazilian_restaurant', 'lebanese_restaurant', 'middle_eastern_restaurant',
    'mediterranean_restaurant', 'vegan_restaurant', 'vegetarian_restaurant', 'afghani_restaurant',
    'acai_shop', 'cat_cafe', 'dog_cafe', 'shopping_mall',
]

activity_types = [
    'tourist_attraction', 'point_of_interest', 'museum', 'art_gallery', 'zoo', 'aquarium', 'park',
    'farm', 'national_park', 'state_park', 'botanical_garden', 'water_park', 'wildlife_park',
    'wildlife_refuge', 'amusement_park', 'amusement_center', 'roller_coaster', 'ferris_wheel',
    'hiking_area', 'camping_cabin', 'playground', 'bowling_alley', 'casino', 'movie_theater',
    'concert_hall', 'theater', 'opera_house', 'philharmonic_hall', 'planetarium', 'marina',
    'picnic_ground', 'off_roading_area', 'adventure_sports_center', 'childrens_camp',
    'community_center', 'visitor_center', 'event_venue', 'wedding_venue', 'monument',
    'historical_place', 'historical_landmark', 'cultural_center', 'cultural_landmark',
    'religious_site', 'church', 'synagogue', 'mosque', 'hindu_temple', 'library', 'art_studio',
    'dance_hall', 'comedy_club', 'karaoke', 'video_arcade', 'internet_cafe', 'banquet_hall',
    'auditorium'
]

# ACCOMMODATION
def get_accommodations_from_destination(request, destination_id):
    accommodations = Accommodation.objects.filter(destination_id=destination_id)
    data = []
    for accommodation in accommodations:
        images = AccommodationImage.objects.filter(accommodation=accommodation)
        images_data = [img.uri for img in images]
        accommodation_data = {
            'accommodation': AcommodationSerializer(accommodation).data,
            'images': images_data
        } 
          
        data.append(accommodation_data)
    return JsonResponse({'accommodations': data}, safe=False)

@csrf_exempt
def create_accommodation_with_images(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        place_id = data.get('place_id')
        destination_id = data.get('destination')
        name = data.get('name')
        primary_type = data.get('primary_type') or 'hotel'
        rating = data.get('rating')
        formatted_address = data.get('formattedAddress')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        images = data.get('images', [])
        is_save = data.get('isSave')

        destination = Destination.objects.get(pk=destination_id)

        accommodation = Accommodation.objects.create(
            place_id=place_id,
            destination=destination,
            name=name,
            accomodation_type=primary_type,
            rating=rating,
            address=formatted_address,
            latitude=latitude,
            longitude=longitude,
            isSave=is_save
        )

        for uri in images:
            AccommodationImage.objects.create(
                accommodation=accommodation,
                uri=uri
            )

        return JsonResponse({'status': 'ok', 'id accommodation': accommodation.place_id})
    return JsonResponse({'error': 'Método no permitido :('}, status=405)


# ACTIVITY
def get_activities_from_destination(request, destination_id):
    activities = Activity.objects.filter(destination_id=destination_id)
    data = []
    for activity in activities:
        images = ActivityImage.objects.filter(activity=activity)
        images_data = [img.uri for img in images]
        activity_data = {
            'activity': ActivitySerializer(activity).data,
            'images': images_data
        }
        data.append(activity_data)
    return JsonResponse({'activities': data}, safe=False)

@csrf_exempt
def create_activity_with_images(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        place_id = data.get('place_id')
        destination_id = data.get('destination')
        name = data.get('name')
        primary_type = data.get('primary_type') or 'tourist_attraction'
        rating = data.get('rating')
        formatted_address = data.get('formattedAddress')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        images = data.get('images', [])
        is_save = data.get('isSave')

        destination = Destination.objects.get(pk=destination_id)

        activity = Activity.objects.create(
            place_id=place_id,
            destination=destination,
            name=name,
            activity_type=primary_type,
            rating=rating,
            address=formatted_address,
            latitude=latitude,
            longitude=longitude,
            isSave=is_save
        )

        for uri in images:
            ActivityImage.objects.create(
                activity=activity,
                uri=uri
            )

        return JsonResponse({'status': 'ok', 'id activity': activity.place_id})
    return JsonResponse({'error': 'Método no permitido :('}, status=405)


# RESTAURANT
def get_restaurants_from_destination(request, destination_id):
    restaurants = Restaurant.objects.filter(destination_id=destination_id)
    data = []
    for restaurant in restaurants:
        images = RestaurantImage.objects.filter(restaurant=restaurant)
        images_data = [img.uri for img in images]
        restaurant_data = {
            'restaurant': RestaurantSerializer(restaurant).data,
            'images': images_data
        }
        data.append(restaurant_data)
    return JsonResponse({'restaurants': data}, safe=False)

@csrf_exempt
def create_restaurant_with_images(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        place_id = data.get('place_id')
        destination_id = data.get('destination')
        name = data.get('name')
        primary_type = data.get('primary_type') or 'restaurant'
        rating = data.get('rating')
        formatted_address = data.get('formattedAddress')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        images = data.get('images', [])
        is_save = data.get('isSave')

        destination = Destination.objects.get(pk=destination_id)

        restaurant = Restaurant.objects.create(
            place_id=place_id,
            destination=destination,
            name=name,
            restaurant_type=primary_type,
            rating=rating,
            address=formatted_address,
            latitude=latitude,
            longitude=longitude,
            isSave=is_save
        )

        for uri in images:
            RestaurantImage.objects.create(
                restaurant=restaurant,
                uri=uri
            )

        return JsonResponse({'status': 'ok', 'id restaurante': restaurant.place_id})
    return JsonResponse({'error': 'Método no permitido :('}, status=405)

# SAVED PLACES
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_saved_place_with_images(request):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        place_id = request.data.get('place_id')
        name = request.data.get('name')
        primary_type = request.data.get('primary_type')
        rating = request.data.get('rating')
        formatted_address = request.data.get('formattedAddress')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        isSave = request.data.get('isSave')
        images = request.data.get('images', [])

        try:
            user = User.objects.get(pk=user_id)
        except:
            return JsonResponse({'error' : 'Usuario no encontrado'}, status=404)
        
        if SavedPlace.objects.filter(user=user, place_id=place_id).exists():
            return JsonResponse({'error': 'Este lugar ya está guardado'}, status=400)
        
        saved_place = SavedPlace.objects.create(
            user=user,
            place_id=place_id,
            name=name,
            rating=rating,
            address=formatted_address,
            place_type=primary_type,
            latitude=latitude,
            longitude=longitude,
            isSave=isSave,
        )

        for uri in images:
            SavedPlaceImage.objects.create(
                saved_place=saved_place,
                uri=uri
            )

        return JsonResponse({'status': 'ok', 'id accommodation': saved_place.savedPlaces_id})
    return JsonResponse({'error': 'Método no permitido :('}, status=405)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_saved_places_by_category(request, user_id):

    
    saved_places = SavedPlace.objects.filter(user_id=user_id)
    accommodations = []
    restaurants = []
    activities = []   
     
    for place in saved_places:
        images = SavedPlaceImage.objects.filter(saved_place=place)
        images_data = [img.uri for img in images]
        place_data = {
            'saved_place': SavedPlacesSerializer(place).data,
            'images': images_data
        }
        if place.place_type in accommodation_types:
            accommodations.append(place_data)
        elif place.place_type in restaurant_types:
            restaurants.append(place_data)
        elif place.place_type in activity_types:
            activities.append(place_data)

    return JsonResponse({
        'accommodations': accommodations,
        'restaurants': restaurants,
        'activities': activities,
    }, safe=False)
    
# SAVED PLACES - Alojamientos
def get_saved_accommodations(request, user_id):

    saved_places = SavedPlace.objects.filter(user_id=user_id, place_type__in=accommodation_types)
    data = []
    for place in saved_places:
        images = SavedPlaceImage.objects.filter(saved_place=place)
        images_data = [img.uri for img in images]
        data.append({
            'saved_place': SavedPlacesSerializer(place).data,
            'images': images_data
        })
    return JsonResponse({'saved_accommodations': data}, safe=False)


# SAVED PLACES - Restauración / Gastronomía
def get_saved_restaurants(request, user_id):

    saved_places = SavedPlace.objects.filter(user_id=user_id, place_type__in=restaurant_types)
    data = []
    for place in saved_places:
        images = SavedPlaceImage.objects.filter(saved_place=place)
        images_data = [img.uri for img in images]
        data.append({
            'saved_place': SavedPlacesSerializer(place).data,
            'images': images_data
        })
    return JsonResponse({'saved_restaurants': data}, safe=False)


# SAVED PLACES - Actividades / Turismo
def get_saved_activities(request, user_id):
    
    saved_places = SavedPlace.objects.filter(user_id=user_id, place_type__in=activity_types)
    data = []
    for place in saved_places:
        images = SavedPlaceImage.objects.filter(saved_place=place)
        images_data = [img.uri for img in images]
        data.append({
            'saved_place': SavedPlacesSerializer(place).data,
            'images': images_data
        })
    return JsonResponse({'saved_activities': data}, safe=False)


# API GOOGLE PLACES
@csrf_exempt
@require_POST
def google_places_search_nearby(request):
    api_key = PLACES_API_KEY
    data = json.loads(request.body)
    
    lat = data.get('latitude', 39.576003)
    lng = data.get('longitude', 2.654179)
    radius = data.get('radius', 50000)
    category = data.get('category', 'Alojamientos')
    user_id = data.get('user_id')  # <-- Recibe el user_id del frontend
    category = category.strip().lower() 

    match category:
        case "alojamientos":
            included_types = [
                "lodging", "hotel", "motel", "bed_and_breakfast", "guest_house", "hostel"
            ]
        case "comer y beber":
            included_types = [
                "restaurant", "bar", "cafe", "bakery", "pub", "fast_food_restaurant", "buffet_restaurant"
            ]
        case "cosas que hacer":
            included_types = [
                "tourist_attraction", "museum", "art_gallery", "zoo", "aquarium", "park", "amusement_park", "night_club", 
                 "church", "mosque"
            ]
        case _:
            included_types = []

    payload = {
        "includedTypes": included_types,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": lat,
                    "longitude": lng
                },
                "radius": radius
            }
        },
    }
    headers = {
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.location,places.rating,places.priceLevel,places.websiteUri,places.primaryType,places.types,places.regularOpeningHours,places.photos,places.nationalPhoneNumber"
    }

    url = f"https://places.googleapis.com/v1/places:searchNearby?key={api_key}"
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    from apps.places.models.saved_place import SavedPlace
    saved_place_ids = set()
    if user_id:
        saved_place_ids = set(SavedPlace.objects.filter(user_id=user_id).values_list('place_id', flat=True))

    for place in data.get('places', []):
        place['isSave'] = place.get('id') in saved_place_ids
    return JsonResponse(data, safe=False)


# RECIBIR TODAS LAS CATEGORIAS A PARTIR DEL ID DEL DESTINO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_all_categories_from_destination(request):
    if request.method == "POST":
        destination_id = request.data.get('destination_id')
        if not destination_id:
            return JsonResponse({'error': 'destination_id es requerido'}, status=400)
        try: 
            destination = Destination.objects.get(pk=destination_id)
        except Destination.DoesNotExist:
            return JsonResponse({'error': 'Destination no encontrado'}, status=400)
        
        destination_data = DestinationSerializer(destination).data
        
        # ALOJAMIENTOS
        accommodations = Accommodation.objects.filter(destination=destination)
        accommodations_data = []
        for alj in accommodations:
            images = AccommodationImage.objects.filter(accommodation=alj)
            images_data = [img.uri for img in images]
            accommodations_data.append({
                'accommodation': alj.name,
                'id': alj.place_id,
                'accommodaton_type': alj.accomodation_type,
                'address': alj.address,
                'rating': alj.rating if alj.rating is not None else 3.0,
                'latitude': alj.latitude,
                'longitude': alj.longitude,
                'images': images_data,
                'isSave': alj.isSave,
            })
            
        # RESTAURANTES     
        restaurants = Restaurant.objects.filter(destination=destination)
        restaurants_data = []
        for rest in restaurants:
            images = RestaurantImage.objects.filter(restaurant=rest)
            images_data = [img.uri for img in images]
            restaurants_data.append({
                'restaurant': rest.name,
                'id': rest.place_id,
                'restaurant_type': rest.restaurant_type,
                'rating': rest.rating if rest.rating is not None else 3.0,
                'address': rest.address,
                'latitude': rest.latitude,
                'longitude': rest.longitude,
                'images': images_data,
                'isSave': rest.isSave,
            })

        # ACTIVIDADES
        activities = Activity.objects.filter(destination=destination)
        activities_data = []
        for act in activities:
            images = ActivityImage.objects.filter(activity=act)
            images_data = [img.uri for img in images]
            activities_data.append({
                'activity': act.name,
                'place_id': act.place_id,
                'activity_type': act.activity_type,
                'rating': act.rating if act.rating is not None else 3.0,
                'address': act.address,
                'latitude': act.latitude,
                'longitude': act.longitude,
                'images': images_data,
                'isSave': act.isSave,
            })
            
        return JsonResponse({
            'destination': destination_data,
            'accommodations': accommodations_data,
            'restaurants': restaurants_data,
            'activities': activities_data,
        })
    


from apps.places.shared_imports import *
from django.db import transaction

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
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_accommodations_from_destination(request, destination_id):
    accommodations = Accommodation.objects.filter(destination_id=destination_id)
    data = []
    for accommodation in accommodations:
        images = AccommodationImage.objects.filter(accommodation=accommodation)
        data.append({
            'accommodation': AcommodationSerializer(accommodation).data,
            'images': [img.uri for img in images]
        })
    return JsonResponse({'accommodations': data}, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_accommodation_with_images(request):
    data = request.data
    destination = get_object_or_404(Destination, pk=data.get('destination'))

    with transaction.atomic():
        accommodation = Accommodation.objects.create(
            place_id=data.get('place_id'),
            destination=destination,
            name=data.get('name'),
            accomodation_type=data.get('primary_type') or 'hotel',
            rating=data.get('rating'),
            address=data.get('formattedAddress'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            isSave=data.get('isSave'),
        )
        AccommodationImage.objects.bulk_create([
            AccommodationImage(accommodation=accommodation, uri=uri)
            for uri in (data.get('images') or [])
        ])

    return JsonResponse({'status': 'ok', 'id accommodation': accommodation.place_id}, status=201)


# ACTIVITY
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_activities_from_destination(request, destination_id):
    activities = Activity.objects.filter(destination_id=destination_id)
    data = []
    for activity in activities:
        images = ActivityImage.objects.filter(activity=activity)
        data.append({
            'activity': ActivitySerializer(activity).data,
            'images': [img.uri for img in images]
        })
    return JsonResponse({'activities': data}, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_activity_with_images(request):
    data = request.data
    destination = get_object_or_404(Destination, pk=data.get('destination'))

    with transaction.atomic():
        activity = Activity.objects.create(
            place_id=data.get('place_id'),
            destination=destination,
            name=data.get('name'),
            activity_type=data.get('primary_type') or 'tourist_attraction',
            rating=data.get('rating'),
            address=data.get('formattedAddress'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            isSave=data.get('isSave'),
        )
        ActivityImage.objects.bulk_create([
            ActivityImage(activity=activity, uri=uri)
            for uri in (data.get('images') or [])
        ])

    return JsonResponse({'status': 'ok', 'id activity': activity.place_id}, status=201)


# RESTAURANT
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_restaurants_from_destination(request, destination_id):
    restaurants = Restaurant.objects.filter(destination_id=destination_id)
    data = []
    for restaurant in restaurants:
        images = RestaurantImage.objects.filter(restaurant=restaurant)
        data.append({
            'restaurant': RestaurantSerializer(restaurant).data,
            'images': [img.uri for img in images]
        })
    return JsonResponse({'restaurants': data}, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_restaurant_with_images(request):
    data = request.data
    destination = get_object_or_404(Destination, pk=data.get('destination'))

    with transaction.atomic():
        restaurant = Restaurant.objects.create(
            place_id=data.get('place_id'),
            destination=destination,
            name=data.get('name'),
            restaurant_type=data.get('primary_type') or 'restaurant',
            rating=data.get('rating'),
            address=data.get('formattedAddress'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            isSave=data.get('isSave'),
        )
        RestaurantImage.objects.bulk_create([
            RestaurantImage(restaurant=restaurant, uri=uri)
            for uri in (data.get('images') or [])
        ])

    return JsonResponse({'status': 'ok', 'id restaurante': restaurant.place_id}, status=201)


# SAVED PLACES
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_saved_place_with_images(request):
    data = request.data
    user = get_object_or_404(User, pk=data.get('user_id'))

    if SavedPlace.objects.filter(user=user, place_id=data.get('place_id')).exists():
        return JsonResponse({'error': 'Este lugar ya está guardado'}, status=400)

    with transaction.atomic():
        saved_place = SavedPlace.objects.create(
            user=user,
            place_id=data.get('place_id'),
            name=data.get('name'),
            rating=data.get('rating'),
            address=data.get('formattedAddress'),
            place_type=data.get('primary_type'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            isSave=data.get('isSave'),
        )
        SavedPlaceImage.objects.bulk_create([
            SavedPlaceImage(saved_place=saved_place, uri=uri)
            for uri in (data.get('images') or [])
        ])

    return JsonResponse({'status': 'ok', 'id accommodation': saved_place.savedPlaces_id}, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_saved_places_by_category(request, user_id):
    saved_places = SavedPlace.objects.filter(user_id=user_id)
    accommodations, restaurants, activities = [], [], []

    for place in saved_places:
        images = SavedPlaceImage.objects.filter(saved_place=place)
        place_data = {
            'saved_place': SavedPlacesSerializer(place).data,
            'images': [img.uri for img in images]
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_saved_accommodations(request, user_id):
    saved_places = SavedPlace.objects.filter(user_id=user_id, place_type__in=accommodation_types)
    data = []
    for place in saved_places:
        images = SavedPlaceImage.objects.filter(saved_place=place)
        data.append({
            'saved_place': SavedPlacesSerializer(place).data,
            'images': [img.uri for img in images]
        })
    return JsonResponse({'saved_accommodations': data}, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_saved_restaurants(request, user_id):
    saved_places = SavedPlace.objects.filter(user_id=user_id, place_type__in=restaurant_types)
    data = []
    for place in saved_places:
        images = SavedPlaceImage.objects.filter(saved_place=place)
        data.append({
            'saved_place': SavedPlacesSerializer(place).data,
            'images': [img.uri for img in images]
        })
    return JsonResponse({'saved_restaurants': data}, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_saved_activities(request, user_id):
    saved_places = SavedPlace.objects.filter(user_id=user_id, place_type__in=activity_types)
    data = []
    for place in saved_places:
        images = SavedPlaceImage.objects.filter(saved_place=place)
        data.append({
            'saved_place': SavedPlacesSerializer(place).data,
            'images': [img.uri for img in images]
        })
    return JsonResponse({'saved_activities': data}, safe=False)


# RECIBIR TODAS LAS CATEGORIAS A PARTIR DEL ID DEL DESTINO
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_all_categories_from_destination(request):
    destination_id = request.data.get('destination_id')
    if not destination_id:
        return JsonResponse({'error': 'destination_id es requerido'}, status=400)

    destination = get_object_or_404(Destination, pk=destination_id)
    destination_data = DestinationSerializer(destination).data

    # ALOJAMIENTOS
    accommodations_data = []
    for alj in Accommodation.objects.filter(destination=destination):
        images = AccommodationImage.objects.filter(accommodation=alj)
        accommodations_data.append({
            'accommodation': alj.name,
            'id': alj.place_id,
            'accommodaton_type': alj.accomodation_type,
            'address': alj.address,
            'rating': alj.rating if alj.rating is not None else 3.0,
            'latitude': alj.latitude,
            'longitude': alj.longitude,
            'images': [img.uri for img in images],
            'isSave': alj.isSave,
        })

    # RESTAURANTES
    restaurants_data = []
    for rest in Restaurant.objects.filter(destination=destination):
        images = RestaurantImage.objects.filter(restaurant=rest)
        restaurants_data.append({
            'restaurant': rest.name,
            'id': rest.place_id,
            'restaurant_type': rest.restaurant_type,
            'rating': rest.rating if rest.rating is not None else 3.0,
            'address': rest.address,
            'latitude': rest.latitude,
            'longitude': rest.longitude,
            'images': [img.uri for img in images],
            'isSave': rest.isSave,
        })

    # ACTIVIDADES
    activities_data = []
    for act in Activity.objects.filter(destination=destination):
        images = ActivityImage.objects.filter(activity=act)
        activities_data.append({
            'activity': act.name,
            'place_id': act.place_id,
            'activity_type': act.activity_type,
            'rating': act.rating if act.rating is not None else 3.0,
            'address': act.address,
            'latitude': act.latitude,
            'longitude': act.longitude,
            'images': [img.uri for img in images],
            'isSave': act.isSave,
        })

    return JsonResponse({
        'destination': destination_data,
        'accommodations': accommodations_data,
        'restaurants': restaurants_data,
        'activities': activities_data,
    })

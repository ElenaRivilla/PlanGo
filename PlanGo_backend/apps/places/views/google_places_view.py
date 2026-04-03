from apps.places.shared_imports import *

@csrf_exempt 
@require_POST
def google_places_search_nearby(request):
    api_key = PLACES_API_KEY
    req_data = json.loads(request.body) 

    lat = req_data.get('latitude', 39.576003)
    lng = req_data.get('longitude', 2.654179)
    radius = req_data.get('radius', 50000)
    category = req_data.get('category', 'Alojamientos')
    user_id = req_data.get('user_id')

    included_types = google_places_service.map_category_to_types(category)
    payload = google_places_service.build_search_payload(lat, lng, radius, included_types)

    headers = {
        "X-Goog-FieldMask": (
            "places.id,places.displayName,places.formattedAddress,places.location,"
            "places.rating,places.priceLevel,places.websiteUri,places.primaryType,"
            "places.types,places.regularOpeningHours,places.photos,places.nationalPhoneNumber"
        )
    }

    url = f"https://places.googleapis.com/v1/places:searchNearby?key={api_key}"
    response = requests.post(url, json=payload, headers=headers)
    api_response = response.json()

    saved_place_ids = set()
    if user_id:
        saved_place_ids = set(SavedPlace.objects.filter(user_id=user_id).values_list('place_id', flat=True))

    google_places_service.attach_is_save_flag_to_places(api_response, saved_place_ids)
    return JsonResponse(api_response, safe=False)
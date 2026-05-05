from apps.places.shared_imports import *
from apps.places.services import overpass_service


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def google_places_search_nearby(request):
    lat = request.data.get('latitude', 39.576003)
    lng = request.data.get('longitude', 2.654179)
    radius = request.data.get('radius', 10000)
    category = request.data.get('category', 'Alojamientos')
    user_id = request.data.get('user_id')

    try:
        # Buscar lugares con Overpass (OSM)
        places = overpass_service.search_nearby(lat, lng, radius, category)

    except Exception as e:
        print(f"[ERROR] Exception in search_nearby: {type(e).__name__}: {e}")
        return Response({'places': []}, status=status.HTTP_200_OK)

    saved_place_ids = set()
    if user_id:
        saved_place_ids = set(SavedPlace.objects.filter(user_id=user_id).values_list('place_id', flat=True))

    overpass_service.attach_is_save_flag(places, saved_place_ids)
    return Response({'places': places})

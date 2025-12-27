from .shared_imports import *
from .DTO.itinerary_dto import map_itineraries, map_itinerary
GEONAMES_API_KEY = settings.GEONAMES_API_KEY  

def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrftoken': token})  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_itineraries(request):
    itineraries = Itinerary.objects.all()
    
    if not itineraries.exists():
        return JsonResponse({'error': 'No itineraries created'}, status=404)
    
    data = map_itineraries(itineraries)
    return JsonResponse({'itineraries': data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])   
def get_itineraries_by_user(request, user_id):
    itineraries = Itinerary.objects.filter(creator_user=user_id)
    
    if not itineraries.exists():
        return JsonResponse({'error': 'No itineraries created for this user.'}, status=404)
    
    data = map_itineraries(itineraries)
    return JsonResponse({'itineraries': data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_itinerary_by_id(request, itinerary_id):
    try:
        itinerary = Itinerary.objects.get(pk=itinerary_id, creator_user=request.user)
        
        data = map_itinerary(itinerary)
        return JsonResponse(data, safe=False)
    
    except Itinerary.DoesNotExist:
        return JsonResponse({'error': 'Itinerary not found or you do not have permission to access it.'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_countries_by_itinerary(request, itinerary_id):
    try:
        itinerary = Itinerary.objects.get(pk=itinerary_id)
        countries_str = itinerary.countries or ''
        countries_list = [c.strip() for c in countries_str.split(',') if c.strip()]
        return Response({'countries': countries_list})
    
    except Itinerary.DoesNotExist:
        return Response({'error': 'Itinerary not found'}, status=404)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def create_itinerary(request):
    serializer = FormItinerarySerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        itinerary = serializer.save()
        return Response(map_itinerary(itinerary), status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
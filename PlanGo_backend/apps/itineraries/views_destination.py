from .shared_imports import *
from .DTO.destination_dto import map_destinations
GEONAMES_API_KEY = settings.GEONAMES_API_KEY  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_destinations(request):
    destination = Destination.objects.all()
    
    if not destination.exists():
        return JsonResponse({'error': 'No destinations created'}, status=404)
    
    data = map_destinations(destination)
    return JsonResponse({'destination': data}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_destinations_by_itinerary(request, itinerary_id):
    destination = Destination.objects.filter(itinerary=itinerary_id)
    
    if not destination.exists():
        return JsonResponse({'error': 'No destinations created for this user.'}, status=404)
    
    data = map_destinations(destination)
    return JsonResponse({'User destinations': data}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_destination(request):
    data = request.data
    itinerary_id = data.get('itinerary')
    try:
        itinerary = Itinerary.objects.get(pk=itinerary_id)
    except Itinerary.DoesNotExist:
        return JsonResponse({'error': f'Itinerary with id {itinerary_id} does not exist.'}, status=404)

    destinations = Destination.objects.filter(itinerary=itinerary).order_by('-end_date')
    
    if destinations.exists():
        last_end_date = destinations.last().end_date
        start_date = last_end_date + timedelta(days=1)
    else:
        start_date = itinerary.start_date
    end_date = start_date

    payload = {
        'itinerary': itinerary.pk,
        'country': data.get('country'),
        'city_name': data.get('city_name'),
        'start_date': start_date,
        'end_date': end_date,
        'latitude': data.get('latitude'),
        'longitude': data.get('longitude'),
    }

    serializer = DestinationSerializer(data=payload)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        destination = serializer.save()

    destination_data = map_destinations([destination])[0]
    return JsonResponse({'status': 'ok', 'destination': destination_data}, status=201)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_destination(request, destination_id):
    try:
        destination = Destination.objects.get(pk=destination_id)
    except Destination.DoesNotExist:
        return Response({'error': 'Destination not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = DestinationSerializer(destination, data=request.data, partial=True)
    
    if serializer.is_valid():
        destination = serializer.save()
        destination_data = map_destinations([destination])[0]
        return Response(destination_data, status=status.HTTP_200_OK)
    
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
    }, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_countries_by_destination(request, destination_id):
    try:
        destination = Destination.objects.get(pk=destination_id)
        itinerary = destination.itinerary
        countries_str = itinerary.countries or ''
        countries_list = [c.strip() for c in countries_str.split(',') if c.strip()]
        return Response({'countries': countries_list, 'itinerary_id': itinerary.itinerary_id}, status=200)
    except Destination.DoesNotExist:
        return Response({'error': 'Destination not found'}, status=404)

# google_places_autocomplete (GET público)
@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def geocodenames_autocomplete(request):
    input_text = request.GET.get('input')
    country_code = request.GET.get('country')

    if not input_text or not country_code:
        return JsonResponse({'error': 'Missing input or country'}, status=400)

    url = (
        f'http://api.geonames.org/searchJSON'
        f'?name_startsWith={input_text}&country={country_code}&featureClass=P&minPopulation=5000&maxRows=1000&username={GEONAMES_API_KEY}&lang=es'
    )
    response = requests.get(url)
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to serch in GeoNames API'}, status=response.status_code)

    return JsonResponse(response.json(), status=200)
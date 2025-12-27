# core/secrets/api_key.py
from django.http import JsonResponse
import os

def get_google_places_key(request):
    api_key = os.environ.get('PLAN_GO_API_PLACES_KEY', '')
    return JsonResponse({'googlePlacesApiKey': api_key})
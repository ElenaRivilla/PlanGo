from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
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
from rest_framework.decorators import authentication_classes
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.conf import settings
import requests
import json
import os
from .services import google_places_service
PLACES_API_KEY = settings.API_KEY

__all__ = [
    "api_view", "permission_classes", "IsAuthenticated", "status", "Response",
    "render", "get_object_or_404", "JsonResponse", "Accommodation", "User",
    "AcommodationSerializer", "ActivitySerializer", "RestaurantSerializer", "SavedPlacesSerializer",
    "DestinationSerializer", "AccommodationImage", "Activity", "ActivityImage",
    "Destination", "Restaurant", "RestaurantImage", "SavedPlace", "SavedPlaceImage",
    "csrf_exempt", "authentication_classes", "require_POST", "settings", "requests", "json", "os",
    "PLACES_API_KEY", "google_places_service", "get_token"
]
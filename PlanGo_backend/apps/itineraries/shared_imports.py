from datetime import timedelta
import requests
import pycountry

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.utils import timezone
from django.views import View
from django.db import models
from django.db.models import Sum
from django.db import transaction

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

# Modelos y serializadores de la app
from .serializer import ItinerarySerializer, DestinationSerializer, FormItinerarySerializer
from apps.itineraries.models.itinerary import Itinerary
from apps.itineraries.models.destination import Destination
from apps.places.models.accommodation import Accommodation
from apps.places.models.activity import Activity
from apps.places.models.restaurant import Restaurant
from apps.expenses.models.expense import Expense
from apps.users.models.user import User

__all__ = [
    "render", "JsonResponse", "HttpResponse", "settings", "timezone", "View",
    "models", "Sum", "transaction", "Response", "status",
    "api_view", "permission_classes", "IsAuthenticated", "AllowAny",
    "require_http_methods", "require_POST", "require_GET", "method_decorator",
    "csrf_exempt", "get_token",
    "timedelta", "requests", "pycountry",
    "ItinerarySerializer", "DestinationSerializer", "FormItinerarySerializer",
    "Itinerary", "Destination", "Accommodation", "Activity", "Restaurant", "Expense", "User",
]
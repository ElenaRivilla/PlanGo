from django.urls import path
from .views import get_google_places_key

urlpatterns = [
    path('google-places-key/', get_google_places_key, name='google_places_key'),
]
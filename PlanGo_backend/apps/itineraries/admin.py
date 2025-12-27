from django.contrib import admin
from apps.itineraries.models.destination import Destination
from apps.itineraries.models.itinerary import Itinerary

# Registrar los modelos en el admin
admin.site.register(Destination) 
admin.site.register(Itinerary) 
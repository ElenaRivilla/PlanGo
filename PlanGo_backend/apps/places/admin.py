from django.contrib import admin
from apps.places.models.accommodation import Accommodation
from apps.places.models.accommodation_image import AccommodationImage
from apps.places.models.activity import Activity
from apps.places.models.activity_image import ActivityImage
from apps.places.models.restaurant import Restaurant
from apps.places.models.restaurant_image import RestaurantImage
from apps.places.models.saved_place import SavedPlace
from apps.places.models.saved_place_image import SavedPlaceImage

# Register your models here.
admin.site.register(Accommodation)
admin.site.register(AccommodationImage)
admin.site.register(Activity)
admin.site.register(ActivityImage)
admin.site.register(Restaurant)
admin.site.register(RestaurantImage)
admin.site.register(SavedPlace)
admin.site.register(SavedPlaceImage)
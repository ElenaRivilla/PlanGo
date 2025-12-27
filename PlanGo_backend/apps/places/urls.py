from django.urls import path
from .views import get_accommodations_from_destination, get_activities_from_destination, get_restaurants_from_destination, get_saved_accommodations, get_saved_activities, get_saved_restaurants, google_places_search_nearby, create_activity_with_images, create_restaurant_with_images, create_accommodation_with_images, create_saved_place_with_images, get_all_categories_from_destination, get_saved_places_by_category

urlpatterns = [
    # ITINERARY
    path('accommodations/<int:destination_id>/', get_accommodations_from_destination, name='get_accommodations_from_destination'),
    path('activities/<int:destination_id>/', get_activities_from_destination, name='get_activities_from_destination'),
    path('restaurants/<int:destination_id>/', get_restaurants_from_destination, name='get_restaurants_from_destination'),

    # SAVED PLACES
    path('saved_accommodations/<int:user_id>/', get_saved_accommodations, name='get_saved_accommodations'),
    path('saved_restaurants/<int:user_id>/', get_saved_restaurants, name='get_saved_restaurants'),
    path('saved_activities/<int:user_id>/', get_saved_activities, name='get_saved_activities'),
    path('saved_places/by_category/<int:user_id>/', get_saved_places_by_category, name='get_saved_places_by_category'),

    # CREATE ACCOMMODATION
    path('create_accommodation/', create_accommodation_with_images, name="create_accommodation_with_images"),
    
    # CREATE RESTAURANT
    path('create_restaurant/', create_restaurant_with_images, name="create_restaurant_with_images"),
    
    # CREATE ACTIVITY
    path('create_activity/', create_activity_with_images, name="create_activity_with_images"),
    
     # CREATE SAVED PLACE
    path('create_saved_place/', create_saved_place_with_images, name="create_saved_place_with_images"),
    
    # GIVE ALL CATEGORIES FROM A DESTIONATION
    path('get_categories/', get_all_categories_from_destination, name="get_all_categories_from_destination"),
    
    # API PLACES 
    path('google_places_search_nearby/', google_places_search_nearby, name='google_places_search_nearby'),
]
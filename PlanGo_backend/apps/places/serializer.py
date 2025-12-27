from rest_framework import serializers
from apps.places.models.accommodation import Accommodation
from apps.places.models.activity import Activity
from apps.places.models.restaurant import Restaurant
from apps.places.models.saved_place import SavedPlace


class AcommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = '__all__'
        
        
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
      
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
      
class SavedPlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPlace
        fields = '__all__'
      
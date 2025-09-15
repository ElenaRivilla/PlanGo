import json
from rest_framework import serializers
from .models.itinerary import Itinerary
from .models.destination import Destination
from django.utils import timezone

class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = '__all__'
               
class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'
      
class FormItinerarySerializer(serializers.ModelSerializer):
    countries = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = Itinerary
        fields = ['itinerary_name', 'creator_user', 'creation_date', 'start_date', 'end_date', 'countries']

    def create(self, validated_data):
        countries = validated_data.pop('countries', [])
        validated_data['countries'] = ','.join(countries)
        itinerary = Itinerary.objects.create(**validated_data)
        return itinerary
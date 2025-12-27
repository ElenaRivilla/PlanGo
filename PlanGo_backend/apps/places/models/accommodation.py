from django.db import models
from apps.itineraries.models.destination import Destination

class Accommodation(models.Model):
    place_id = models.CharField(max_length=255, primary_key=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='accommodations')
    name = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    address = models.TextField()
    ACCOMMODATION_TYPES = [
        ('bed_and_breakfast', 'Bed and Breakfast'),
        ('budget_japanese_inn', 'Budget Japanese Inn'),
        ('campground', 'Campground'),
        ('camping_cabin', 'Camping Cabin'),
        ('cottage', 'Cottage'),
        ('extended_stay_hotel', 'Extended Stay Hotel'),
        ('farmstay', 'Farmstay'),
        ('guest_house', 'Guest House'),
        ('hostel', 'Hostel'),
        ('hotel', 'Hotel'),
        ('inn', 'Inn'),
        ('japanese_inn', 'Japanese Inn'),
        ('lodging', 'Lodging'),
        ('mobile_home_park', 'Mobile Home Park'),
        ('motel', 'Motel'),
        ('private_guest_room', 'Private Guest Room'),
        ('resort_hotel', 'Resort Hotel'),
        ('rv_park', 'RV Park'),
    ]
    accomodation_type = models.CharField(max_length=50, choices=ACCOMMODATION_TYPES)
    latitude = models.DecimalField(max_digits=30, decimal_places=20)
    longitude = models.DecimalField(max_digits=30, decimal_places=20)
    isSave = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Accommodation'
        verbose_name_plural = 'Accommodation'
            
    def __str__(self):
        return self.name
from django.db import models
from .itinerary import Itinerary

class Destination(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='destinations')
    country = models.CharField(max_length=150)
    city_name = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.city_name}, {self.country}"
from django.db import models
from apps.users.models.user import User

class Itinerary(models.Model):
    itinerary_id = models.AutoField(primary_key=True)
    itinerary_name = models.CharField(max_length=255)
    creator_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itineraries')
    creation_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    countries = models.TextField()  # Almacena el JSON como string

    class Meta:
        verbose_name = 'Itinerary'
        verbose_name_plural = 'Itinerary'

    def __str__(self):
        return f"Itinerary #{self.itinerary_id} by {self.creator_user}"
from django.db import models
from users.models.user import User

class Itinerary(models.Model):
    itinerary_id = models.AutoField(primary_key=True)
    creator_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itineraries')
    creator_first_name = models.CharField(max_length=255)
    creation_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Itinerary #{self.id} by {self.creator_first_name}"
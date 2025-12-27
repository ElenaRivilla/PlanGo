from django.db import models
from ...itineraries.models.destination import Destination
from apps.users.models.user import User

class Participant(models.Model):
    participant_id = models.AutoField(primary_key=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='participations')
    participant_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Participant'
        verbose_name_plural = 'Participant'
            
    def __str__(self):
        return f"{self.participant_name}, {self.destination}"
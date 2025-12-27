from django.db import models
from .accommodation import Accommodation

class AccommodationImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    accommodation = models.ForeignKey(Accommodation, to_field='place_id', db_column='place_id', on_delete=models.CASCADE, related_name='images')
    uri = models.TextField()
    
    class Meta:
        verbose_name = 'Accommodation Image'
        verbose_name_plural = 'Accommodation Image'
        
        
    def __int__(self):
        return self.accommodation
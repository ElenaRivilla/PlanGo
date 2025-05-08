from  django.db import models 
from .saved_place import SavedPlace

class SavedPlaceImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    saved_place = models.ForeignKey(SavedPlace, on_delete=models.CASCADE, related_name='images')
    uri = models.TextField()
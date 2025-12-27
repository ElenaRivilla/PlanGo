from  django.db import models 
from .saved_place import SavedPlace

class SavedPlaceImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    saved_place = models.ForeignKey(SavedPlace, on_delete=models.CASCADE, related_name='images')
    uri = models.TextField()
    
    class Meta:
        verbose_name = 'Saved Place Image'
        verbose_name_plural = 'Saved Place Image'
        
    def __int__(self):
        return self.saved_place
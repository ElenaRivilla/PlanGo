from django.db import models
from .restaurant import Restaurant

class RestaurantImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, to_field='place_id', db_column='place_id', on_delete=models.CASCADE, related_name='images')
    uri = models.TextField()
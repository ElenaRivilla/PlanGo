from django.db import models
from .activity import Activity

class ActivityImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    activity = models.ForeignKey(Activity, to_field='place_id', db_column='place_id', on_delete=models.CASCADE, related_name='images')
    uri = models.TextField()
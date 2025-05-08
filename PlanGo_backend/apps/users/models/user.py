from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100) # modificar estos datos en la base de datos
    last_name = models.CharField(max_length=100)  # modificar estos datos en la base de datos
    email = models.EmailField(unique=True)
    user_image = models.TextField(blank=True, null=True)
    countries_visited = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
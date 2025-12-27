from django.contrib import admin
from apps.users.models import User
from apps.users.models.participant import Participant

# Registrar el modelo Usuario en el admin
admin.site.register(User)
admin.site.register(Participant) 

from django.db import models
from itineraries.models.destination import Destination
from users.models.user import User

class Expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=255, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(blank=True, null=True)
    paid_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='paid_expenses')
    paid_by_name = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.description
from django.db import models
#from itineraries.models.destination import Destination
from apps.users.models.user import User
from apps.itineraries.models.destination import Destination

class Expense(models.Model):
    TYPE_EXPENSE = [
        ('Equalitarian', 'Equalitarian'),
        ('Personalized', 'Personalized'),
    ]
    expense_id = models.AutoField(primary_key=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='expenses', null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(blank=True, null=True)
    paid_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='paid_expenses')
    paid_by_name = models.CharField(max_length=100, blank=True, null=True)
    type_expense = models.CharField(max_length=20, choices=TYPE_EXPENSE, default='Personalized')


    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expense'
        
    def __str__(self):
        return self.description or f"Expense {self.expense_id}"
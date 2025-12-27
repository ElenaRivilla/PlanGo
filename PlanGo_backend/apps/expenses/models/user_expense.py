from django.db import models
from apps.expenses.models.expense import Expense
from apps.users.models.user import User

class UserExpense(models.Model):
    user_expense_id = models.AutoField(primary_key=True)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='user_expenses')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='user_expenses')
    user_name = models.CharField(max_length=100, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    expected_share = models.DecimalField(max_digits=10, decimal_places=2)
    debt = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'UserExpense'
        verbose_name_plural = 'UserExpense'
        
        
    def __str__(self):
        return self.expense.description
    
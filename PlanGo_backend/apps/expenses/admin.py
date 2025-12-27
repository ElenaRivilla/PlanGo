from django.contrib import admin
from apps.expenses.models.expense import Expense
from apps.expenses.models.user_expense import UserExpense

# Register your models here.
admin.site.register(Expense)
admin.site.register(UserExpense)
from rest_framework import serializers
from apps.expenses.models.expense import Expense
from apps.expenses.models.user_expense import UserExpense

class ExpenseSerializer(serializers.ModelSerializer):
        class Meta: 
            model = Expense
            fields = '__all__'
            

class UserExpenseSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = UserExpense
        fields = ['user_expense_id', 'expense', 'user', 'user_name', 'amount_paid', 'expected_share', 'debt']

    def get_user_name(self, obj):
        if obj.user:
            return obj.user.username
        return obj.user_name
    

class ExpenseWithNamesSerializer(serializers.ModelSerializer):
    itinerary_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    paid_by_name = serializers.SerializerMethodField()
    user_expenses = UserExpenseSerializer(many=True, read_only=True)

    class Meta:
        model = Expense
        fields = [
            'expense_id', 'description', 'total_amount', 'date',
            'paid_by_user', 'paid_by_name', 'type_expense',
            'itinerary_name', 'city_name', 'user_expenses'
        ]

    def get_itinerary_name(self, obj):
        if obj.destination and obj.destination.itinerary:
            return obj.destination.itinerary.itinerary_name
        return None

    def get_city_name(self, obj):
        if obj.destination:
            return obj.destination.city_name
        return None

    def get_paid_by_name(self, obj):
        # Si es invitado, ya tienes el nombre
        if obj.paid_by_name:
            return obj.paid_by_name
        # Si es usuario registrado, busca el nombre de usuario
        if obj.paid_by_user:
            try:
                return obj.paid_by_user.username
            except AttributeError:
                return None
        return None
    
    
class InsertExpenseSerializer(serializers.ModelSerializer):
    user_Expense = serializers.SerializerMethodField()
    
    class Meta: 
        model = Expense
        fields = ['expense_id', 'description', 'total_amount', 'date', 'paid_by_user', 'paid_by_name', 'type_expense', 'itinerary_name', 'destination_name', 'user_expense_id', 'user', 'user_name', 'amount_paid', 'expected_share', 'debt']

    def get_User_Expenses(self, obj):
        if obj.userexpense:
            return obj
        return None
    
# resultado = {
#     expense_id: auto,
#     date: today,
#     itinerary_name: string,
#     destination_name: string,
#     paid_by_user: number,
#     paid_by_name: string,
#     total_amount: float,
#     description: string,
#     user: number maybe null, 
#     user_name: string maybe null,
#     expected_share: float, 
#     debt: float,
      
# }
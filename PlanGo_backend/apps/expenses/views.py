from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from .serializer import ExpenseSerializer, UserExpenseSerializer, ExpenseWithNamesSerializer
from apps.expenses.models.expense import Expense
from apps.itineraries.models.itinerary import Itinerary
from apps.expenses.models.user_expense import UserExpense
from apps.itineraries.models.destination import Destination
from apps.users.models.participant import Participant
from apps.users.models.user import User
from django.db.models import Q
import json





# Create your views here.
# EXPENSE
def get_expenses(request):
    expenses = Expense.objects.all()
    if not expenses.exists():
        return JsonResponse({'error': 'No hay gastos creados'}, status=404)
    data = [
        {
            'expense_id': i.expense_id,
            'destination': i.destination.id if i.destination else None,
            'description': i.description,
            'total_amount': i.total_amount,
            'date': i.date,
            'paid_by_user': i.paid_by_user.id if i.paid_by_user else None,
            'paid_by_name': i.paid_by_name,
            'type_expense': i.type_expense,
        }
        for i in expenses
    ]
    return JsonResponse({'expenses': data})

def get_expenses_by_destination(request, destination_id):
    destexpenses = Expense.objects.filter(destination_id=destination_id)
    if not destexpenses.exists():
        return JsonResponse({'error' : 'No hay gastos realizados en este destino'}, status=404)
    
    data = [
        {
            'expense_id': i.expense_id,
            'description' : i.description,
            'destination': i.destination.id if i.destination else None,
            'total_amount': i.total_amount,
            'date': i.date,
            'paid_by_user': i.paid_by_user.id if i.paid_by_user else None,
            'paid_by_name': i.paid_by_name,
            'type_expense': i.type_expense,
        }
        for i in destexpenses
    ]
    return JsonResponse({'destination expenses': data})
        
    
# USEREXPENSE
def get_user_expenses(request):
    user_expenses = UserExpense.objects.all()
    if not user_expenses.exists():
        return JsonResponse({'error': 'No hay usuarios con gastos creados'}, status=404)
    data = [
        {
            'user_expense_id': i.user_expense_id,
            'expense_id': i.expense.expense_id if hasattr(i.expense, 'expense_id') else i.expense,
            'user_id': i.user.id if hasattr(i.user, 'id') else i.user,
            'user_name': i.user_name,
            'amount_paid': i.amount_paid,
            'expected_share': i.expected_share,
            'debt': i.debt,
        }
        for i in user_expenses
    ]   
    return JsonResponse({'user expenses': data})
    

def get_user_expenses_by_expense_id(request, expense_id):
    user_expenses = UserExpense.objects.filter(expense_id=expense_id)
    if not user_expenses.exists():
        return JsonResponse({'error': 'No hay usuario con gastos en este gasto.'}, status=404)
    data = [
        {
            'user_expense_id': i.user_expense_id,
            'expense_id': i.expense.expense_id if hasattr(i.expense, 'expense_id') else i.expense,
            'user_id': i.user.id if hasattr(i.user, 'id') else i.user,
            'user_name': i.user_name,
            'amount_paid': i.amount_paid,
            'expected_share': i.expected_share,
            'debt': i.debt,

        }
        for i in user_expenses
    ]    
    return JsonResponse({'user expenses': data})


# EXPENSE - USEREXPENSE

def expenses_with_users(request, destination_id):
    expenses = Expense.objects.filter(destination=destination_id)

    if not expenses.exists():
        return JsonResponse({'error' : 'No hay gastos realizados en este destino'}, status=404)
    
    for expense in expenses:
        # Filtrar UserExpenses relacionados a este expense específico
        users_expenses = UserExpense.objects.filter(expense=expense.expense_id)
        
        if not users_expenses.exists():
            return JsonResponse({'error' : 'No hay gastos realizados en este destino'}, status=404)
        
    data = []
    for expense in expenses:
        user_expense_data = [
            {
                'user_expense_id': ue.user_expense_id,
                'expense_id': ue.expense.expense_id,
                'user_id': ue.user.id if hasattr(ue.user, 'id') else ue.user,
                'user_name': ue.user_name,
                'amount_paid': ue.amount_paid,
                'expected_share': ue.expected_share,
                'debt': ue.debt,
            }
            for ue in users_expenses
        ]
    
    user_expenses_calculated = (expense.type_expense, user_expense_data, expense.total_amount)
    
    data.append({
            'expense_id': expense.expense_id,
            'destination': expense.destination.id if expense.destination else None,
            'description': expense.description,
            'total_amount': expense.total_amount,
            'date': expense.date,
            'paid_by_user': expense.paid_by_user.id if expense.paid_by_user else None,
            'paid_by_name': expense.paid_by_name,
            'type_expense': expense.type_expense,
            'user_expenses' : user_expenses_calculated
        })
    return JsonResponse({'expenses with user expenses': data})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_expense_with_users(request):
    data = request.data
    user_expenses_data = data.pop('user_expenses', [])
    expense_serializer = ExpenseSerializer(data=data)
    if expense_serializer.is_valid():
        expense = expense_serializer.save()
        for ue_data in user_expenses_data:
            ue_data['expense'] = expense.expense_id
            ue_serializer = UserExpenseSerializer(data=ue_data)
            if ue_serializer.is_valid():
                ue_serializer.save()
            else:
                return Response(ue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(expense_serializer.data, status=status.HTTP_201_CREATED)
    return Response(expense_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_expenses_with_names(request):
    expenses = Expense.objects.all()
    serializer = ExpenseWithNamesSerializer(expenses, many=True)
    return JsonResponse({'expenses': serializer.data})


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_expenses_with_names_by_user(request):
    user = request.user
    if not user or not user.is_authenticated:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)
    
    itineraries = Itinerary.objects.filter(creator_user=user)
    expenses = Expense.objects.filter(destination__itinerary__in=itineraries).distinct()
    serializer = ExpenseWithNamesSerializer(expenses, many=True)
    return JsonResponse({'expenses': serializer.data})

@csrf_exempt
def create_expense(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            destination_id = data.get('destination')
            description = data.get('description')
            total_amount = data.get('total_amount')
            date = data.get('date')
            type_expense = data.get('type_expense')
            paid_by_user = data.get('paid_by_user')
            paid_by_name = data.get('paid_by_name')
            debtors = data.get('debtors', [])


            # Obtener instancia de destino
            destination = Destination.objects.get(pk=destination_id)

            # Obtener instancia de usuario si existe
            user_obj = None
            if paid_by_user:
                user_obj = User.objects.get(pk=paid_by_user)

           # Crear el gasto
            expense = Expense.objects.create(
                destination=destination,
                description=description,
                total_amount=total_amount,
                date=date,
                type_expense=type_expense,
                paid_by_user=user_obj if user_obj else None,
                paid_by_name=paid_by_name if not user_obj else None
            )

            match type_expense:
                case 'Personalized':
                    total_expenses = sum(float(debtor.get('amount', 0)) for debtor in debtors)
                    # UserExpense del pagador
                    if user_obj:
                        UserExpense.objects.create(
                            expense=expense,
                            user=user_obj,
                            user_name=None,
                            amount_paid=total_amount,
                            expected_share=float(total_amount) - total_expenses,
                            debt=float(total_amount) - total_expenses
                        )
                    elif paid_by_name:
                        UserExpense.objects.create(
                            expense=expense,
                            user=None,
                            user_name=paid_by_name,
                            amount_paid=total_amount,
                            expected_share=float(total_amount) - total_expenses,
                            debt=float(total_amount) - total_expenses
                        )
                    for debtor in debtors:
                        debtor_user_id = debtor.get('user')
                        debtor_name = debtor.get('user_name')
                        debtor_amount = float(debtor.get('amount', 0))
                        # Si hay user, busca el objeto User, si no, deja None
                        debtor_user = User.objects.get(pk=debtor_user_id) if debtor_user_id else None

                        UserExpense.objects.create(
                            expense=expense,
                            user=debtor_user,
                            user_name=debtor_name,
                            amount_paid=0,
                            expected_share=debtor_amount,
                            debt= debtor_amount
                        )
                    
                    return JsonResponse({'success': True, 'expense_id': expense.expense_id}, status=201)

                case 'Equalitarian':
                    participants_count = len(debtors) + 1
                    share_expense = round(float(total_amount) / participants_count, 2)
                    # UserExpense del pagador
                    if user_obj:
                        UserExpense.objects.create(
                            expense=expense,
                            user=user_obj,
                            user_name=None,
                            amount_paid=total_amount,
                            expected_share=share_expense,
                            debt=float(total_amount) - share_expense,
                        )
                    elif paid_by_name:
                        UserExpense.objects.create(
                            expense=expense,
                            user=None,
                            user_name=paid_by_name,
                            amount_paid=total_amount,
                            expected_share=share_expense,
                            debt=float(total_amount) - share_expense,
                        )
                    for debtor in debtors:
                        debtor_user_id = debtor.get('user')
                        debtor_name = debtor.get('user_name')
                        # Si hay user, busca el objeto User, si no, deja None
                        debtor_user = User.objects.get(pk=debtor_user_id) if debtor_user_id else None

                        UserExpense.objects.create(
                            expense=expense,
                            user=debtor_user,
                            user_name=debtor_name,
                            amount_paid=0,
                            expected_share=share_expense,
                            debt= share_expense,
                        )
                    return JsonResponse({'success': True, 'expense_id': expense.expense_id}, status=201)

                case _:
                    return JsonResponse({'error': 'Tipo de gasto no válido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        

@csrf_exempt
def get_expense_detail(request, expense_id):
    try:
        expense = Expense.objects.get(pk=expense_id)
        serializer = ExpenseWithNamesSerializer(expense)
        
        return JsonResponse({'success': True, 'Gasto': serializer.data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
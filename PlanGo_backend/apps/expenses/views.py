from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .serializer import ExpenseSerializer, UserExpenseSerializer, ExpenseWithNamesSerializer
from apps.expenses.models.expense import Expense
from apps.itineraries.models.itinerary import Itinerary
from apps.expenses.models.user_expense import UserExpense
from apps.itineraries.models.destination import Destination
from apps.users.models.user import User
import json
from .DTO.expenses_dto import map_expense, map_expenses, map_user_expense

# EXPENSE
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_expenses(request):
    expenses = Expense.objects.all()
    if not expenses.exists():
        return JsonResponse({'error': 'No hay gastos creados'}, status=404)
    return JsonResponse({'expenses': map_expenses(expenses)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_expenses_by_destination(request, destination_id):
    destexpenses = Expense.objects.filter(destination_id=destination_id)
    if not destexpenses.exists():
        return JsonResponse({'error' : 'No hay gastos realizados en este destino'}, status=404)
    return JsonResponse({'destination expenses': map_expenses(destexpenses)})
         
# USEREXPENSE
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_expenses(request):
    user_expenses = UserExpense.objects.all()
    if not user_expenses.exists():
        return JsonResponse({'error': 'No hay usuarios con gastos creados'}, status=404)
    data = [map_user_expense(ue) for ue in user_expenses]
    return JsonResponse({'user expenses': data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_expenses_by_expense_id(request, expense_id):
    user_expenses = UserExpense.objects.filter(expense_id=expense_id)
    if not user_expenses.exists():
        return JsonResponse({'error': 'No hay usuario con gastos en este gasto.'}, status=404)
    data = [map_user_expense(ue) for ue in user_expenses]
    return JsonResponse({'user expenses': data})


# EXPENSE - USEREXPENSE
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expenses_with_users(request, destination_id):
    expenses = Expense.objects.filter(destination=destination_id)
    if not expenses.exists():
        return JsonResponse({'error' : 'No hay gastos realizados en este destino'}, status=404)

    data = []
    for expense in expenses:
        # obtiene los user expenses relacionados
        users_expenses = UserExpense.objects.filter(expense=expense)
        users_data = [map_user_expense(ue) for ue in users_expenses]
        expense_dict = map_expense(expense, include_user_expenses=False)
        expense_dict['user_expenses'] = users_data
        data.append(expense_dict)

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_expenses_with_names(request):
    expenses = Expense.objects.all()
    serializer = ExpenseWithNamesSerializer(expenses, many=True)
    return JsonResponse({'expenses': serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_expenses_with_names_by_user(request):
    user = request.user
    if not user or not user.is_authenticated:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)
    
    itineraries = Itinerary.objects.filter(creator_user=user)
    expenses = Expense.objects.filter(destination__itinerary__in=itineraries).distinct()
    serializer = ExpenseWithNamesSerializer(expenses, many=True)
    return JsonResponse({'expenses': serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_expense(request):
    try:
        data = request.data if hasattr(request, 'data') else json.loads(request.body)
        destination_id = data.get('destination')
        description = data.get('description')
        total_amount = float(data.get('total_amount', 0) or 0)
        date = data.get('date')
        type_expense = data.get('type_expense')
        paid_by_user = data.get('paid_by_user')
        paid_by_name = data.get('paid_by_name')
        debtors = data.get('debtors', []) or []

        destination = get_object_or_404(Destination, pk=destination_id)

        user_obj = None
        if paid_by_user:
            user_obj = User.objects.filter(pk=paid_by_user).first()

        with transaction.atomic():
            expense = Expense.objects.create(
                destination=destination,
                description=description,
                total_amount=total_amount,
                date=date,
                type_expense=type_expense,
                paid_by_user=user_obj if user_obj else None,
                paid_by_name=paid_by_name if not user_obj else None
            )

            # Pre-fetch users referenced in debtors to avoid N queries
            debtor_user_ids = {d.get('user') for d in debtors if d.get('user')}
            users_map = {}
            if debtor_user_ids:
                users = User.objects.filter(pk__in=debtor_user_ids)
                users_map = {u.id: u for u in users}

            user_expenses_to_create = []

            def make_payer_ue(expected_share, debt, amount_paid=total_amount):
                if user_obj:
                    return UserExpense(
                        expense=expense,
                        user=user_obj,
                        user_name=None,
                        amount_paid=amount_paid,
                        expected_share=expected_share,
                        debt=debt
                    )
                else:
                    return UserExpense(
                        expense=expense,
                        user=None,
                        user_name=paid_by_name,
                        amount_paid=amount_paid,
                        expected_share=expected_share,
                        debt=debt
                    )

            if type_expense == 'Personalized':
                total_debtors_amount = sum(float(d.get('amount', 0) or 0) for d in debtors)
                payer_expected = round(total_amount - total_debtors_amount, 2)
                payer_debt = round(total_amount - total_debtors_amount, 2)
                user_expenses_to_create.append(make_payer_ue(payer_expected, payer_debt))

                for d in debtors:
                    debtor_user_id = d.get('user')
                    debtor_name = d.get('user_name')
                    debtor_amount = round(float(d.get('amount', 0) or 0), 2)
                    debtor_user = users_map.get(debtor_user_id) if debtor_user_id else None
                    user_expenses_to_create.append(UserExpense(
                        expense=expense,
                        user=debtor_user,
                        user_name=debtor_name,
                        amount_paid=0,
                        expected_share=debtor_amount,
                        debt=debtor_amount
                    ))

            elif type_expense == 'Equalitarian':
                participants_count = max(1, len(debtors) + 1)
                share = round(total_amount / participants_count, 2)
                payer_expected = share
                payer_debt = round(total_amount - share, 2)
                user_expenses_to_create.append(make_payer_ue(payer_expected, payer_debt))

                for d in debtors:
                    debtor_user_id = d.get('user')
                    debtor_name = d.get('user_name')
                    debtor_user = users_map.get(debtor_user_id) if debtor_user_id else None
                    user_expenses_to_create.append(UserExpense(
                        expense=expense,
                        user=debtor_user,
                        user_name=debtor_name,
                        amount_paid=0,
                        expected_share=share,
                        debt=share
                    ))
            else:
                return JsonResponse({'error': 'Tipo de gasto no válido'}, status=400)

            # Bulk create reduces DB round-trips
            UserExpense.objects.bulk_create(user_expenses_to_create)
            return JsonResponse({'success': True, 'expense_id': expense.expense_id}, status=201)

    except Destination.DoesNotExist:
        return JsonResponse({'error': 'Destino no encontrado'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_expense_detail(request, expense_id):
    try:
        expense = Expense.objects.get(pk=expense_id)
        return JsonResponse({'success': True, 'Gasto': map_expense(expense, include_user_expenses=True)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
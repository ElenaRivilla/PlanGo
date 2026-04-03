from dataclasses import dataclass, asdict
from typing import Optional, List, Iterable
from datetime import date, datetime

@dataclass
class UserExpenseDTO:
    user_expense_id: int
    expense_id: int
    user_id: Optional[int]
    user_name: Optional[str]
    amount_paid: float
    expected_share: float
    debt: float

@dataclass
class ExpenseDTO:
    expense_id: int
    destination: Optional[int]
    description: Optional[str]
    total_amount: float
    date: Optional[str]
    paid_by_user: Optional[int]
    paid_by_name: Optional[str]
    type_expense: Optional[str]
    user_expenses: Optional[List[dict]] = None

def _iso(d: Optional[date | datetime]) -> Optional[str]:
    if d is None:
        return None
    try:
        return d.isoformat()
    except Exception:
        return str(d)

def map_user_expense(ue) -> dict:
    return asdict(UserExpenseDTO(
        user_expense_id=getattr(ue, 'user_expense_id', None),
        expense_id=getattr(getattr(ue, 'expense', None), 'expense_id', getattr(ue, 'expense', None)),
        user_id=getattr(getattr(ue, 'user', None), 'id', ue.user if hasattr(ue, 'user') else None),
        user_name=getattr(ue, 'user_name', None),
        amount_paid=float(getattr(ue, 'amount_paid', 0) or 0),
        expected_share=float(getattr(ue, 'expected_share', 0) or 0),
        debt=float(getattr(ue, 'debt', 0) or 0),
    ))

def map_expense(expense, include_user_expenses: bool = False) -> dict:
    ue_list = None
    if include_user_expenses:
        from apps.expenses.models.user_expense import UserExpense
        users = UserExpense.objects.filter(expense=expense)
        ue_list = [map_user_expense(u) for u in users]
    return asdict(ExpenseDTO(
        expense_id=getattr(expense, 'expense_id', None),
        destination=getattr(getattr(expense, 'destination', None), 'id', None),
        description=getattr(expense, 'description', None),
        total_amount=float(getattr(expense, 'total_amount', 0) or 0),
        date=_iso(getattr(expense, 'date', None)),
        paid_by_user=getattr(getattr(expense, 'paid_by_user', None), 'id', None),
        paid_by_name=getattr(expense, 'paid_by_name', None),
        type_expense=getattr(expense, 'type_expense', None),
        user_expenses=ue_list
    ))

def map_expenses(expenses: Iterable, include_user_expenses: bool = False) -> List[dict]:
    return [map_expense(e, include_user_expenses) for e in expenses]
export interface Expenses {
    expense_id: number;
    itinerary_id: number;
    itinerary_name: string;
    city_name: string; 
    destination: string;
    description: string;
    total_amount: number;
    date: Date;
    paid_by_user: number;
    paid_by_name: string;
    user_expenses: UserExpenses
    type_expense: string;
  }

export interface UserExpenses {
    user_expense_id: number;
    expense: number;
    user: number;
    user_name: string;
    amount_paid: number;
    debt?: number;
    expected_share: number;
}
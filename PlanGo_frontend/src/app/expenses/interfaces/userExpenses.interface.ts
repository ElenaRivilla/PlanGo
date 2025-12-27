export interface UserExpense {
    user: number;
    user_name: string;
    amount_paid: number;
    expected_share: number;
    debt: number;
}

export interface UserExpenses {
    user_expenses: UserExpense[];
}
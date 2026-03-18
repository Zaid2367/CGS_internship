from collections import defaultdict
from datetime import date
from calendar import monthrange
from sqlalchemy.orm import Session
from models import Transaction
def get_monthly_summary(db: Session, user_id: int, year: int, month: int):
    start_date = date(year, month, 1)
    end_date = date(year, month, monthrange(year, month)[1])
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).filter(Transaction.date >= start_date, Transaction.date <= end_date).all()
    total_income = 0.0
    total_expenses = 0.0
    income_by_category = defaultdict(float)
    expenses_by_category = defaultdict(float)
    for t in transactions:
        if t.type.lower() == "income":
            total_income += t.amount
            income_by_category[t.category or "Uncategorized"] += t.amount
        elif t.type.lower() == "expense":
            total_expenses += t.amount
            expenses_by_category[t.category or "Uncategorized"] += t.amount
    net_balance = total_income - total_expenses
    incomebd = [{"category": cat, "total": amt} for cat, amt in income_by_category.items()]
    expensesbd = [{"category": cat, "total": amt} for cat, amt in expenses_by_category.items()]
    incomebd.sort(key=lambda x: x["total"], reverse=True)
    expensesbd.sort(key=lambda x: x["total"], reverse=True)
    return {
        "year": year,
        "month": month,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": net_balance,
        "income_by_category": incomebd,
        "expenses_by_category": expensesbd
    }
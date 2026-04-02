from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List, Literal
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=50)
class Token(BaseModel):
    access_token: str
    token_type: str
class TransactionCreate(BaseModel):
    title: str
    amount: float
    category: str
    type: Literal["income", "expense"]
    date: date
class TransactionUpdate(BaseModel):
    title: str
    amount: float
    category: str
    type: Literal["income", "expense"]
    date: date
class TransactionOut(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    type: str
    date: date
    class Config:
        from_attributes = True
class categorybd(BaseModel):
    category: str
    total: float
class monthlysummary(BaseModel):
    year: int
    month: int
    total_income: float
    total_expenses: float
    net_balance: float
    income_by_category: List[categorybd]
    expenses_by_category: List[categorybd]

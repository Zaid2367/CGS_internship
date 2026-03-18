from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import Transaction, User
from schemas import TransactionCreate, TransactionUpdate, UserCreate, Token, monthlysummary
from auth import hash_password, verify_password, create_access_token, get_current_user
from service import get_monthly_summary
from datetime import date
from utils import log_req
from exception import UserExistsE, EmailExistsE, InvalidCredentialsE ,TransactionNotFoundE
from logg import logger
Base.metadata.create_all(bind=engine)
app = FastAPI()
@app.exception_handler(UserExistsE)
async def user_exists_handler(request, exc):
    logger.warning(f"User already exists: {exc.message}")
    return JSONResponse(status_code=400, content={"detail": exc.message})
@app.exception_handler(EmailExistsE)
async def email_exists_handler(request, exc):
    logger.warning(f"Email already exists: {exc.message}")
    return JSONResponse(status_code=400, content={"detail": exc.message})
@app.exception_handler(InvalidCredentialsE)
async def invalid_credentials_handler(request, exc):
    logger.warning(f"Invalid credentials: {exc.message}")
    return JSONResponse(status_code=401, content={"detail": exc.message})
@app.exception_handler(TransactionNotFoundE)
async def transaction_not_found_handler(request, exc):
    logger.warning(f"Transaction not found: {exc.message}")
    return JSONResponse(status_code=404, content={"detail": exc.message})

@app.get("/")
def home():
    return {"message": "running"}
@app.post("/register")
@log_req
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user is not None:
        logger.warning(f"Username already exists: {user.username}")
        raise UserExistsE("Username already exists")
    useremail = db.query(User).filter(User.email == user.email).first()
    if useremail is not None:
        logger.warning(f"Email already exists: {user.email}")
        raise EmailExistsE("Email already exists")
    new_user = User(username=user.username, email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    logger.info(f"User registered successfully: {new_user.username}")
    return {"message": "User registered successfully"}
@app.post("/login", response_model=Token)
@log_req
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if user is None: 
        logger.warning(f"Login failed, Username not found: {form_data.username}")
        raise InvalidCredentialsE("Invalid username or password")
    if not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Login failed, Invalid password for user: {form_data.username}")
        raise InvalidCredentialsE("Invalid username or password")
    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}
@app.get("/curr")
def curr(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username, "email": current_user.email}
@app.post("/transactions")
@log_req
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_transaction = Transaction(title=transaction.title, amount=transaction.amount, category=transaction.category, type=transaction.type, date=transaction.date, user_id=current_user.id)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction
@app.get("/transactions")
@log_req
def get_transactions(category: str | None = None, type: str | None = None, start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)
    if category is not None:
        query = query.filter(Transaction.category == category)
    if type is not None:
        query = query.filter(Transaction.type == type)
    if start_date is not None:
        query = query.filter(Transaction.date >= start_date)
    if end_date is not None:
        query = query.filter(Transaction.date <= end_date)
    return query.all()
@app.get("/transactions/{transaction_id}")
@log_req
def get_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == current_user.id).first()
    if transaction is None:
        logger.warning(f"Transaction not found: {transaction_id} for user {current_user.id}")
        raise TransactionNotFoundE("Transaction not found")
    logger.info(f"Transaction received: {transaction_id} for user {current_user.id}")
    return transaction
@app.put("/transactions/{transaction_id}")
@log_req
def update_transaction(transaction_id: int, updated_data: TransactionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == current_user.id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    transaction.title = updated_data.title
    transaction.amount = updated_data.amount
    transaction.category = updated_data.category
    transaction.type = updated_data.type
    transaction.date = updated_data.date
    db.commit()
    db.refresh(transaction)
    return transaction
@app.delete("/transactions/{transaction_id}")
@log_req
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == current_user.id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}
@app.get("/monthly-summary", response_model=monthlysummary)
@log_req
def monthly_summary(
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_monthly_summary(
        db=db,
        user_id=current_user.id,
        year=year,
        month=month,
    )
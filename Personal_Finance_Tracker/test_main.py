import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app
from database import Base, get_db
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
client = TestClient(app)
def register_user():
    return client.post("/register",
        json={
            "username": "zaid",
            "email": "zaid@example.com",
            "password": "12345678"
        }
    )
def login_user():
    return client.post("/login",
        data={
            "username": "zaid",
            "password": "12345678"
        }
    )
def get_token():
    register_user()
    response = login_user()
    token = response.json()["access_token"]
    return token
def test_register_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/register",
        json={
            "username": "zaid",
            "email": "zaid@example.com",
            "password": "12345678"
        }
    )
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["message"] == "User registered successfully"
def test_login_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    register_user()
    response = login_user()
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
def test_unauthorized_access_to_transactions():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response = client.get("/transactions")
    assert response.status_code == 401
def test_create_transaction():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    token = get_token()
    response = client.post("/transactions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Movie Ticket",
            "amount": 300,
            "category": "movies",
            "type": "expense",
            "date": "2026-03-16"
        }
    )
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["title"] == "Movie Ticket"
    assert data["type"] == "expense"
def test_get_all_transactions():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    token = get_token()
    client.post("/transactions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Salary",
            "amount": 25000,
            "category": "job",
            "type": "income",
            "date": "2026-03-16"
        }
    )
    response = client.get("/transactions", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
def test_invalid_transaction_type():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    token = get_token()
    response = client.post(
        "/transactions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Watch",
            "amount": 2000,
            "category": "shopping",
            "type": "watches",
            "date": "2026-03-16"
        }
    )
    assert response.status_code == 422
def test_update_transaction():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    token = get_token()
    create_response = client.post(
        "/transactions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Bus",
            "amount": 100,
            "category": "travel",
            "type": "expense",
            "date": "2026-03-16"
        }
    )
    transaction_id = create_response.json()["id"]
    response = client.put(
        f"/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Bus Fare",
            "amount": 150,
            "category": "travel",
            "type": "expense",
            "date": "2026-03-16"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Bus Fare"
    assert data["amount"] == 150
def test_delete_transaction():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    token = get_token()
    create_response = client.post(
        "/transactions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Lunch",
            "amount": 250,
            "category": "food",
            "type": "expense",
            "date": "2026-03-16"
        }
    )
    transaction_id = create_response.json()["id"]
    response = client.delete(
        f"/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction deleted successfully"
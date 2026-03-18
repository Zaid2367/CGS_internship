# Personal Finance Tracker API

A backend REST API built with FastAPI for managing personal finances.  
It allows users to register, log in, and manage their transactions securely.

## Features
- User registration and login
- JWT authentication
- Add, view, update, and delete transactions
- SQLite database
- Swagger UI for API testing

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

## Project Structure
```bash
Personal_Finance_Tracker/
│── app/
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth.py
│   ├── exception.py
│   ├── service.py
│   └── logg.py
│── tests/
│── requirements.txt
│── README.md
│── .gitignore
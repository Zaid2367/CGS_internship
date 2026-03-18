from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
from f_config import DATABASE_URL
#base=Path(__file__).resolve().parent
#Database_url = f"sqlite:///{base/'app.db'}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) 
Session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()
def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")  # Берём URL из переменной окружения

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
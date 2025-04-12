from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import APIRouter, Depends
from typing import List

DATABASE_URL = "sqlite:///./todos.db"  # or replace with your actual db

# Database setup
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ✅ This is what you're missing:
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create the router
router = APIRouter()

# Define a simple endpoint for getting todos (replace with your actual logic)
@router.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    # Your logic for fetching todos from the database
    # Example: db.query(Todo).all() if you had a Todo model
    return {"message": "List of todos"}

# Add other routes as needed

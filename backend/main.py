import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

# Load environment variables from the .env file
load_dotenv()

# Get environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todos.db")  # Default to SQLite if not set
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")  # Default to local backend URL if not set

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=database.engine)

# Initialize FastAPI app
app = FastAPI()

# Configure CORS with origins from environment variable
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "*",
    BACKEND_URL,  # Use the BACKEND_URL from the environment variables
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow frontend to access the backend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/todos", response_model=list[schemas.ToDoOut])
def get_todos(status: str = None, db: Session = Depends(get_db)):
    todos = crud.get_all_todos(db)
    if status == "completed":
        return [t for t in todos if t.completed]
    elif status == "pending":
        return [t for t in todos if not t.completed]
    return todos

@app.post("/todos", response_model=schemas.ToDoOut)
def create_todo(todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

@app.put("/todos/{todo_id}", response_model=schemas.ToDoOut)
def update_todo(todo_id: int, todo: schemas.ToDoUpdate, db: Session = Depends(get_db)):
    return crud.update_todo(db, todo_id, todo)

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    crud.delete_todo(db, todo_id)
    return {"detail": "Deleted"}

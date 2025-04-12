from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "*",
     "https://fastapi-rodillon.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow frontend to access the backend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

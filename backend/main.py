from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routes import todos  # Ensure this import is correct

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can limit this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],  # You may want to restrict this further in production
    allow_headers=["*"],
)

# Ensure all tables are created (this assumes your models file has Base and all the necessary ORM models)
models.Base.metadata.create_all(bind=engine)

# Include the router from todos
app.include_router(todos.router)

@app.get("/")
def root():
    return {"message": "API is running"}

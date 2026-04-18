from fastapi import FastAPI
from sqlalchemy import text
from src.database import engine, Base
import src.models

app = FastAPI(title="Grabpic Intelligent Identity & Retrieval Engine")

# Basic health check endpoint for server monitoring and testing connectivity
@app.get("/")
def read_root():
    return {"message": "Welcome to Grabpic API", "status": "online"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Initialize the database and create necessary tables on startup
@app.on_event("startup")
def on_startup():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    Base.metadata.create_all(bind=engine)


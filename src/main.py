from fastapi import FastAPI, BackgroundTasks
from sqlalchemy import text
from src.database import engine, Base
import src.models
from src.ingestion import process_storage_directory
from src.retrieval import router as retrieval_router

app = FastAPI(title="Grabpic Intelligent Identity & Retrieval Engine")
app.include_router(retrieval_router)


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

@app.post("/ingest")
def start_ingestion(background_tasks: BackgroundTasks):
    """
    Crawls the /storage directory to process images and map them to identities.
    Triggers as a background task to prevent timing out the web request.
    """
    background_tasks.add_task(process_storage_directory)
    return {"message": "Ingestion started in the background."}

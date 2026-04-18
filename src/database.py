import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load variables from .env file into the environment
load_dotenv()

# Use the Docker service name 'db' default, or localhost if running locally
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@localhost:5432/grabpic")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

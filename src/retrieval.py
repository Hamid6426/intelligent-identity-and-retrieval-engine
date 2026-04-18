import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from deepface import DeepFace
from src.database import get_db
from src.models import Person, FaceEmbedding, Image
from dotenv import load_dotenv

load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "Facenet512")
DISTANCE_THRESHOLD = float(os.getenv("DISTANCE_THRESHOLD", "0.30"))

router = APIRouter()

@router.post("/authenticate")
async def authenticate_selfie(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Selfie Authentication:
    Takes an uploaded image containing a face, and acts as a key to find the internal 'grab_id'.
    """
    # Save the incoming file to a temporary location for DeepFace to process
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        faces = DeepFace.represent(img_path=temp_path, model_name=MODEL_NAME, enforce_detection=False)
        
        if not faces or (isinstance(faces, list) and not faces[0].get('face_confidence', 0)):
            raise HTTPException(status_code=400, detail="No face detected in the provided image.")
            
        embedding = faces[0].get("embedding")
        
        # Query PGVector for the closest match
        match = db.query(
            FaceEmbedding, 
            FaceEmbedding.embedding.cosine_distance(embedding).label("distance")
        ).order_by("distance").first()
        
        if match and match.distance < DISTANCE_THRESHOLD:
            return {
                "message": "Authentication successful",
                "grab_id": str(match.FaceEmbedding.person_id),
                "distance": match.distance
            }
        else:
            raise HTTPException(status_code=404, detail="Identity not found in the database. Are you registered?")
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.get("/images/{grab_id}")
def get_user_images(grab_id: str, db: Session = Depends(get_db)):
    """
    Data Extraction endpoint: Fetch all images where this person (grab_id) appears.
    """
    person = db.query(Person).filter(Person.id == grab_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Invalid grab_id")
        
    images = set()
    for face in person.faces:
        images.add(face.image.file_path)
            
    return {"grab_id": grab_id, "image_count": len(images), "images": list(images)}

@router.get("/identities")
def list_identities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Utility endpoint to verify what is currently in the database.
    """
    persons = db.query(Person).offset(skip).limit(limit).all()
    results = []
    for p in persons:
        results.append({
            "grab_id": str(p.id),
            "face_appearances": len(p.faces),
            "created_at": p.created_at
        })
    return {"total": len(results), "identities": results}

# --- Database Inspection Endpoints ---

@router.get("/db/persons")
def get_all_persons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Fetch all rows from the Person table."""
    persons = db.query(Person).offset(skip).limit(limit).all()
    return {
        "total": len(persons),
        "data": [{"id": str(p.id), "created_at": p.created_at} for p in persons]
    }

@router.get("/db/images")
def get_all_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Fetch all rows from the Image table."""
    images = db.query(Image).offset(skip).limit(limit).all()
    return {
        "total": len(images),
        "data": [{"id": str(img.id), "file_path": img.file_path, "created_at": img.created_at} for img in images]
    }

@router.get("/db/embeddings")
def get_all_embeddings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Fetch all rows from the FaceEmbedding table (excluding the raw vector array for readability)."""
    embeddings = db.query(FaceEmbedding).offset(skip).limit(limit).all()
    return {
        "total": len(embeddings),
        "data": [{"id": str(e.id), "person_id": str(e.person_id), "image_id": str(e.image_id), "created_at": e.created_at} for e in embeddings]
    }


import os
import glob
from sqlalchemy.orm import Session
from deepface import DeepFace
from src.database import SessionLocal
from src.models import Image, Person, FaceEmbedding
from dotenv import load_dotenv

load_dotenv()

STORAGE_DIR = os.getenv("STORAGE_DIR", "storage")
MODEL_NAME = os.getenv("MODEL_NAME", "Facenet512")
DISTANCE_THRESHOLD = float(os.getenv("DISTANCE_THRESHOLD", "0.30"))

def process_file(file_path: str, db: Session):
    existing_image = db.query(Image).filter(Image.file_path == file_path).first()
    if existing_image:
        print(f"Skipping already processed file: {file_path}")
        return
    
    try:
        # Extract features for all faces in image.
        # enforce_detection=False so if no face is found, it doesn't crash the script.
        faces = DeepFace.represent(img_path=file_path, model_name=MODEL_NAME, enforce_detection=False)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return

    # Deepface sometimes returns empty dict or list if no face
    if not faces or (isinstance(faces, list) and not faces[0].get('face_confidence', 0)):
        print(f"No valid face found in {file_path}")
        return

    # Add Image to DB
    img_record = Image(file_path=file_path)
    db.add(img_record)
    db.commit()
    db.refresh(img_record)

    for face_data in faces:
        embedding = face_data.get("embedding")
        if not embedding:
            continue
            
        # Search db for matching face using Cosine Distance
        match = db.query(
            FaceEmbedding, 
            FaceEmbedding.embedding.cosine_distance(embedding).label("distance")
        ).order_by("distance").first()
        
        person_id = None
        if match and match.distance < DISTANCE_THRESHOLD:
            person_id = match.FaceEmbedding.person_id
            print(f"Matched face in {file_path} to Person {person_id} (Distance: {match.distance:.3f})")
        else:
            new_person = Person()
            db.add(new_person)
            db.commit()
            db.refresh(new_person)
            person_id = new_person.id
            print(f"Created new Person Identity {person_id} for face in {file_path}")

        # Map face embedding to person and image
        new_face = FaceEmbedding(person_id=person_id, image_id=img_record.id, embedding=embedding)
        db.add(new_face)
        db.commit()

def process_storage_directory():
    print("Starting ingestion crawler...")
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

    db = SessionLocal()
    try:
        valid_extensions = ["*.jpg", "*.jpeg", "*.png"]
        files = []
        for ext in valid_extensions:
            files.extend(glob.glob(os.path.join(STORAGE_DIR, "**", ext), recursive=True))
        
        for file in files:
            process_file(file, db)
    finally:
        db.close()
    print("Ingestion complete.")

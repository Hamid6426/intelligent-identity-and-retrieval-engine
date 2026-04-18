import uuid
import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from src.database import Base

class Person(Base):
    __tablename__ = "persons"
    
    # This id acts as the grab_id
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    faces = relationship("FaceEmbedding", back_populates="person")

class Image(Base):
    __tablename__ = "images"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    file_path = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    faces = relationship("FaceEmbedding", back_populates="image")

class FaceEmbedding(Base):
    __tablename__ = "face_embeddings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=False)
    image_id = Column(UUID(as_uuid=True), ForeignKey("images.id"), nullable=False)
    
    # Assuming DeepFace's "Facenet-512" model which generates a 512-dim vector.
    # If you decide to use standard "Facenet", this would be 128.
    embedding = Column(Vector(512), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    person = relationship("Person", back_populates="faces")
    image = relationship("Image", back_populates="faces")

"""
Workflow model for storing workflow metadata
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime

class Workflow(Base):
    __tablename__ = "workflows"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False, index=True)  # References Session
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    workflow_type = Column(String(50), default="agentic_rag")  # agentic_rag, corrective_rag, etc.
    status = Column(String(50), default="created")  # created, running, completed, error
    vector_store_path = Column(String(500), nullable=True)  # Path to vector store
    collection_name = Column(String(255), nullable=True)  # ChromaDB collection name
    node_count = Column(Integer, nullable=True)  # Number of nodes in the vector store
    embedding_model = Column(String(100), nullable=True)  # Embedding model used
    llm_model = Column(String(100), nullable=True)  # LLM model used
    workflow_metadata = Column(JSON, nullable=True)  # Additional workflow metadata
    error_message = Column(Text, nullable=True)  # Error details if workflow fails
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    session = relationship("Session", backref="workflow")

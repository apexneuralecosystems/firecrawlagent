"""
ChatMessage model for storing chat history
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False, index=True)  # References Session
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    role = Column(String(20), nullable=False)  # user, assistant, system
    message = Column(Text, nullable=False)  # The message content
    response = Column(Text, nullable=True)  # Assistant response (if role is assistant)
    tokens_used = Column(Integer, nullable=True)  # Number of tokens used for this message
    processing_time = Column(String(50), nullable=True)  # Time taken to process (e.g., "1.23s")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    session = relationship("Session", back_populates="messages")

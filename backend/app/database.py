"""
Database configuration using SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Database URL from environment variable, default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# If we are using asyncpg in the env var (for Apex/FastAPI), we need to replace it 
# with psycopg2 (or clean postgresql://) for this synchronous engine
SYNC_DATABASE_URL = DATABASE_URL.replace("+asyncpg", "+psycopg2") if "+asyncpg" in DATABASE_URL else DATABASE_URL

# Create engine
engine = create_engine(
    SYNC_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SYNC_DATABASE_URL else {},
    echo=True
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

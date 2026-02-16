"""
Database configuration using SQLAlchemy
"""
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

# Load .env from project root (parent of backend/) so DATABASE_URL is set when running from backend/
_project_root = Path(__file__).resolve().parents[2]
load_dotenv(_project_root / ".env")


class Base(DeclarativeBase):
    """Single declarative base for all models — do NOT redefine."""
    pass


# Database URL from environment variable, default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# If we are using asyncpg in the env var (for Apex/FastAPI), we need to replace it
# with psycopg2 (or clean postgresql://) for this synchronous engine
SYNC_DATABASE_URL = DATABASE_URL.replace("+asyncpg", "+psycopg2") if "+asyncpg" in DATABASE_URL else DATABASE_URL

# Only echo SQL in development when explicitly enabled
_echo_sql = os.getenv("SQL_ECHO", "false").lower() in ("1", "true", "yes")

# Engine keyword arguments — differ between SQLite and PostgreSQL
_is_sqlite = "sqlite" in SYNC_DATABASE_URL
_engine_kwargs: dict = {
    "echo": _echo_sql,
}
if _is_sqlite:
    _engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    # Production-grade connection pool settings for PostgreSQL
    _engine_kwargs.update({
        "pool_size": int(os.getenv("DB_POOL_SIZE", "5")),
        "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "10")),
        "pool_timeout": 30,
        "pool_pre_ping": True,  # Verify connections are alive before use
    })

# Create engine
engine = create_engine(SYNC_DATABASE_URL, **_engine_kwargs)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

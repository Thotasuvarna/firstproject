"""
Database Engine & Session Management.
Supports MySQL enterprise deployment and SQLite local quickstart.
"""
import logging
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

logger = logging.getLogger("app.database")

Base = declarative_base()


def get_engine():
    """
    Initializes database engine based on settings.
    Uses SQLite locally for zero-config execution and MySQL for production.
    """
    db_url = settings.DATABASE_URL
    if db_url.startswith("sqlite"):
        engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False},
            echo=False
        )
        dialect = "SQLite"
    else:
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False
        )
        dialect = "MySQL"
        
    logger.info(f"[Database] Engine configured with dialect: {dialect} ({db_url})")
    return engine, dialect


engine, ACTIVE_DB_DIALECT = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Creates all database tables defined in the SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)
    logger.info(f"[Database] Tables verified and created on dialect: {ACTIVE_DB_DIALECT}")

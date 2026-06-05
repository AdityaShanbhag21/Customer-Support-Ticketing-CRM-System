"""
database.py
-----------
Configures the SQLite database connection using SQLAlchemy.
Creates the engine, session factory, and base class for all ORM models.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# SQLite database file will be created in the project root
DATABASE_URL = "sqlite:///./crm.db"

# Create the SQLAlchemy engine
# check_same_thread=False is required for SQLite when used with FastAPI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal is a factory that creates new database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    All models must inherit from this class.
    """
    pass


def get_db():
    """
    Dependency function for FastAPI routes.
    Yields a database session and ensures it is closed after the request.

    Usage in a route:
        @app.get("/example")
        def example(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

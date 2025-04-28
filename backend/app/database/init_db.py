"""
Database initialization module.
"""
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.orm import Session

from app.database.session import engine
from app.models.user import Base
from app.core.config import settings


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable foreign keys for SQLite."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def init_db() -> None:
    """Initialize database by creating all tables."""
    # Create tables
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session."""
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    print("Database tables created.")

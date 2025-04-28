"""
User model definition.
"""
from sqlalchemy import Column, Integer, String, Boolean

from app.database.session import Base


class User(Base):
    """SQLAlchemy User model following FastAPI best practices."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

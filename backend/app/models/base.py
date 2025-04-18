from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.db import Base

class BaseModel(Base):
    """
    Base model for common fields across all models.
    Intended to be inherited by all other models.
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 
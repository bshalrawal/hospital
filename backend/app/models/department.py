"""
Department model.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Department(Base):
    """Department model for organizing equipment."""

    __tablename__ = "department"

    department_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    department_name = Column(String(100), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    equipment = relationship("Equipment", back_populates="department", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Department(id={self.department_id}, name='{self.department_name}')>"

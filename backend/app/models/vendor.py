"""
Vendor model.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Vendor(Base):
    """Vendor model for equipment suppliers."""

    __tablename__ = "vendor"

    vendor_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    vendor_name = Column(String(200), nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    category = Column(String(100), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    equipment = relationship("Equipment", back_populates="vendor")

    def __repr__(self) -> str:
        return f"<Vendor(id={self.vendor_id}, name='{self.vendor_name}')>"

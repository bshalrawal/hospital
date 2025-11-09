"""
Discard Equipment model.
"""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class DiscardEquipment(Base):
    """Discard Equipment model for tracking discarded equipment."""

    __tablename__ = "discard_equipment"

    discard_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.equipment_id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    reason = Column(Text, nullable=False)
    media_url = Column(String(500), nullable=True)
    date = Column(Date, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    equipment = relationship("Equipment", back_populates="discard_record")

    def __repr__(self) -> str:
        return f"<DiscardEquipment(id={self.discard_id}, equipment_id={self.equipment_id})>"

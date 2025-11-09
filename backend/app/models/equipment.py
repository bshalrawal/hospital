"""
Equipment model.
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.enums import EquipmentStatus


class Equipment(Base):
    """Equipment model for hospital equipment tracking."""

    __tablename__ = "equipment"

    equipment_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    equipment_name = Column(String(200), nullable=False, index=True)
    serial_number = Column(String(100), nullable=True, unique=True, index=True)
    model_no = Column(String(100), nullable=True)
    manufacturer = Column(String(200), nullable=True, index=True)
    department_id = Column(Integer, ForeignKey("department.department_id", ondelete="RESTRICT"), nullable=False, index=True)
    purchase_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True, index=True)
    status = Column(Enum(EquipmentStatus), nullable=False, default=EquipmentStatus.WORKING, index=True)
    vendor_id = Column(Integer, ForeignKey("vendor.vendor_id", ondelete="RESTRICT"), nullable=True, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="check_quantity_positive"),
    )

    # Relationships
    department = relationship("Department", back_populates="equipment")
    vendor = relationship("Vendor", back_populates="equipment")
    issue_reports = relationship("IssueReport", back_populates="equipment", cascade="all, delete-orphan")
    discard_record = relationship("DiscardEquipment", back_populates="equipment", uselist=False, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Equipment(id={self.equipment_id}, name='{self.equipment_name}', status='{self.status.value}')>"

from __future__ import annotations

from sqlalchemy import CheckConstraint, Date, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.enums import EquipmentStatus


class Equipment(Base):
    __tablename__ = "equipment"
    __table_args__ = (CheckConstraint("quantity >= 0", name="ck_equipment_quantity_non_negative"),)

    equipment_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    equipment_name: Mapped[str] = mapped_column(String(200), nullable=False)
    serial_number: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)
    model_no: Mapped[str | None] = mapped_column(String(100), nullable=True)
    manufacturer: Mapped[str | None] = mapped_column(String(200), nullable=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("department.department_id", ondelete="RESTRICT"), nullable=False)
    purchase_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    expiry_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    status: Mapped[EquipmentStatus] = mapped_column(
        Enum(EquipmentStatus, name="equipment_status"), default=EquipmentStatus.WORKING, nullable=False
    )
    vendor_id: Mapped[int | None] = mapped_column(ForeignKey("vendor.vendor_id", ondelete="SET NULL"), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    department = relationship("Department", back_populates="equipment")
    vendor = relationship("Vendor", back_populates="equipment")
    issue_reports = relationship("IssueReport", back_populates="equipment", cascade="all, delete-orphan")
    discard_record = relationship(
        "DiscardEquipment",
        back_populates="equipment",
        uselist=False,
        cascade="all, delete-orphan",
    )

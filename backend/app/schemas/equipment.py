"""
Equipment Pydantic schemas.
"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from app.models.enums import EquipmentStatus
from app.schemas.department import DepartmentResponse
from app.schemas.vendor import VendorResponse


class EquipmentBase(BaseModel):
    """Base equipment schema."""
    equipment_name: str = Field(..., min_length=1, max_length=200)
    serial_number: Optional[str] = Field(None, max_length=100)
    model_no: Optional[str] = Field(None, max_length=100)
    manufacturer: Optional[str] = Field(None, max_length=200)
    department_id: int
    purchase_date: Optional[date] = None
    expiry_date: Optional[date] = None
    status: EquipmentStatus = EquipmentStatus.WORKING
    vendor_id: Optional[int] = None
    quantity: int = Field(default=1, ge=0)

    @field_validator("expiry_date")
    @classmethod
    def validate_expiry_date(cls, v: Optional[date], info) -> Optional[date]:
        """Validate expiry_date is after purchase_date."""
        if v and info.data.get("purchase_date") and v < info.data["purchase_date"]:
            raise ValueError("Expiry date must be after purchase date")
        return v


class EquipmentCreate(EquipmentBase):
    """Schema for creating equipment."""
    pass


class EquipmentUpdate(BaseModel):
    """Schema for updating equipment."""
    equipment_name: Optional[str] = Field(None, min_length=1, max_length=200)
    serial_number: Optional[str] = Field(None, max_length=100)
    model_no: Optional[str] = Field(None, max_length=100)
    manufacturer: Optional[str] = Field(None, max_length=200)
    department_id: Optional[int] = None
    purchase_date: Optional[date] = None
    expiry_date: Optional[date] = None
    status: Optional[EquipmentStatus] = None
    vendor_id: Optional[int] = None
    quantity: Optional[int] = Field(None, ge=0)


class EquipmentResponse(EquipmentBase):
    """Schema for equipment responses."""
    equipment_id: int
    department: Optional[DepartmentResponse] = None
    vendor: Optional[VendorResponse] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class EquipmentListResponse(BaseModel):
    """Schema for equipment list responses (lighter weight)."""
    equipment_id: int
    equipment_name: str
    serial_number: Optional[str]
    department_id: int
    status: EquipmentStatus
    expiry_date: Optional[date]
    created_at: datetime

    model_config = {"from_attributes": True}

"""
Vendor Pydantic schemas.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class VendorBase(BaseModel):
    """Base vendor schema."""
    vendor_name: str = Field(..., min_length=1, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)


class VendorCreate(VendorBase):
    """Schema for creating a vendor."""
    pass


class VendorUpdate(BaseModel):
    """Schema for updating a vendor."""
    vendor_name: Optional[str] = Field(None, min_length=1, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)


class VendorResponse(VendorBase):
    """Schema for vendor responses."""
    vendor_id: int
    created_at: datetime
    updated_at: datetime
    equipment_count: Optional[int] = None

    model_config = {"from_attributes": True}

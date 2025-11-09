"""
Department Pydantic schemas.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class DepartmentBase(BaseModel):
    """Base department schema."""
    department_name: str = Field(..., min_length=1, max_length=100)


class DepartmentCreate(DepartmentBase):
    """Schema for creating a department."""
    pass


class DepartmentUpdate(BaseModel):
    """Schema for updating a department."""
    department_name: Optional[str] = Field(None, min_length=1, max_length=100)


class DepartmentResponse(DepartmentBase):
    """Schema for department responses."""
    department_id: int
    created_at: datetime
    updated_at: datetime
    equipment_count: Optional[int] = None

    model_config = {"from_attributes": True}

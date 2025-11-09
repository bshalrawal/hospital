"""
Discard Equipment Pydantic schemas.
"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class DiscardBase(BaseModel):
    """Base discard schema."""
    equipment_id: int
    reason: str = Field(..., min_length=1)
    media_url: Optional[str] = Field(None, max_length=500)
    date: date

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: date) -> date:
        """Ensure discard date is not in the future."""
        if v > date.today():
            raise ValueError("Discard date cannot be in the future")
        return v


class DiscardCreate(DiscardBase):
    """Schema for creating a discard record."""
    pass


class DiscardUpdate(BaseModel):
    """Schema for updating a discard record."""
    reason: Optional[str] = Field(None, min_length=1)
    media_url: Optional[str] = Field(None, max_length=500)
    date: Optional[date] = None


class DiscardResponse(DiscardBase):
    """Schema for discard responses."""
    discard_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

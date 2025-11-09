"""
Issue Report Pydantic schemas.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models.enums import IssueType, IssueStatus


class IssueBase(BaseModel):
    """Base issue schema."""
    equipment_id: int
    issue_type: IssueType
    problem_description: str = Field(..., min_length=1, max_length=2000)
    media_url: Optional[str] = Field(None, max_length=500)
    date_raised: Optional[datetime] = None
    status: IssueStatus = IssueStatus.OPEN
    technician: Optional[str] = Field(None, max_length=100)


class IssueCreate(IssueBase):
    """Schema for creating an issue report."""
    pass


class IssueUpdate(BaseModel):
    """Schema for updating an issue report."""
    issue_type: Optional[IssueType] = None
    problem_description: Optional[str] = Field(None, min_length=1, max_length=2000)
    media_url: Optional[str] = Field(None, max_length=500)
    status: Optional[IssueStatus] = None
    technician: Optional[str] = Field(None, max_length=100)


class IssueResponse(IssueBase):
    """Schema for issue report responses."""
    issue_id: int
    resolved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

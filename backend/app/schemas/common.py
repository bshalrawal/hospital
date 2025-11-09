"""
Common Pydantic schemas used across the API.
"""
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationMeta(BaseModel):
    """Pagination metadata for list responses."""
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")

    model_config = {"from_attributes": True}


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""
    data: List[T]
    pagination: PaginationMeta

    model_config = {"from_attributes": True}


class MessageResponse(BaseModel):
    """Simple message response."""
    message: str
    detail: Optional[str] = None

    model_config = {"from_attributes": True}


class ErrorResponse(BaseModel):
    """Error response format."""
    detail: str
    error_code: Optional[str] = None
    field_errors: Optional[dict] = None

    model_config = {"from_attributes": True}

"""
Schemas package - exports all Pydantic schemas.
"""
from app.schemas.common import PaginationMeta, PaginatedResponse, MessageResponse, ErrorResponse
from app.schemas.user import UserCreate, UserUpdate, UserResponse, LoginRequest, TokenResponse, RefreshTokenResponse
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorResponse
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate, EquipmentResponse, EquipmentListResponse
from app.schemas.issue import IssueCreate, IssueUpdate, IssueResponse
from app.schemas.discard import DiscardCreate, DiscardUpdate, DiscardResponse

__all__ = [
    # Common
    "PaginationMeta",
    "PaginatedResponse",
    "MessageResponse",
    "ErrorResponse",
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "LoginRequest",
    "TokenResponse",
    "RefreshTokenResponse",
    # Department
    "DepartmentCreate",
    "DepartmentUpdate",
    "DepartmentResponse",
    # Vendor
    "VendorCreate",
    "VendorUpdate",
    "VendorResponse",
    # Equipment
    "EquipmentCreate",
    "EquipmentUpdate",
    "EquipmentResponse",
    "EquipmentListResponse",
    # Issue
    "IssueCreate",
    "IssueUpdate",
    "IssueResponse",
    # Discard
    "DiscardCreate",
    "DiscardUpdate",
    "DiscardResponse",
]

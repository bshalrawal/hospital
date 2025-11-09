"""
Issue Report model.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.enums import IssueType, IssueStatus


class IssueReport(Base):
    """Issue Report model for tracking equipment problems."""

    __tablename__ = "issue_report"

    issue_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.equipment_id", ondelete="CASCADE"), nullable=False, index=True)
    issue_type = Column(Enum(IssueType), nullable=False, index=True)
    problem_description = Column(Text, nullable=False)
    media_url = Column(String(500), nullable=True)
    date_raised = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    status = Column(Enum(IssueStatus), nullable=False, default=IssueStatus.OPEN, index=True)
    technician = Column(String(100), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    equipment = relationship("Equipment", back_populates="issue_reports")

    def __repr__(self) -> str:
        return f"<IssueReport(id={self.issue_id}, equipment_id={self.equipment_id}, status='{self.status.value}')>"

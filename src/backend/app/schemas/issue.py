"""Schemas for issue endpoints."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.dataset import IssueType, IssueSeverity


class IssueResponse(BaseModel):
    """Schema for issue response."""
    id: str
    dataset_id: str
    issue_type: IssueType
    severity: IssueSeverity
    column_name: Optional[str]
    description: str
    evidence: dict
    detected_at: datetime
    resolved: bool
    
    class Config:
        from_attributes = True

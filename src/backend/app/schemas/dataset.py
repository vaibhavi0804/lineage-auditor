"""
Pydantic schemas for dataset endpoints.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class DatasetCreate(BaseModel):
    """Schema for creating a dataset."""
    name: str
    description: Optional[str] = None


class DatasetResponse(BaseModel):
    """Schema for dataset response."""
    id: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    row_count: Optional[int]
    column_count: Optional[int]
    
    class Config:
        from_attributes = True


class DatasetProfileResponse(BaseModel):
    """Schema for dataset profile response."""
    id: str
    dataset_id: str
    created_at: datetime
    columns_metadata: dict
    statistics: dict
    
    class Config:
        from_attributes = True

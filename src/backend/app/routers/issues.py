# src/backend/app/routers/issues.py
"""
Issues API router.
"""
from fastapi import APIRouter, HTTPException
from app.supabase_client import table_select
from app.schemas.issue import IssueResponse

# Adjust table name if different
TABLE_ISSUES = "issues"

router = APIRouter()


@router.get("/", response_model=list[IssueResponse])
async def list_issues():
    """List all detected issues."""
    rows = await table_select(TABLE_ISSUES, columns="id,dataset_id,issue_type,details,detected_at", params={"order":"detected_at.desc"})
    return rows


@router.get("/dataset/{dataset_id}", response_model=list[IssueResponse])
async def get_dataset_issues(dataset_id: str):
    """Get issues for a specific dataset."""
    filters = f"dataset_id=eq.{dataset_id}"
    rows = await table_select(TABLE_ISSUES, columns="id,dataset_id,issue_type,details,detected_at", filters=filters, params={"order":"detected_at.desc"})
    return rows

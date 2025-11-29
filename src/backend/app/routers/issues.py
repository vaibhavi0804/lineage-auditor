"""
Issues API router.
Endpoints for detected data quality and schema issues.
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_issues():
    """List all detected issues."""
    return {"issues": []}

"""
Issues API router.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.dataset import Issue
from app.schemas.issue import IssueResponse

router = APIRouter()


@router.get("/", response_model=list[IssueResponse])
async def list_issues(db: Session = Depends(get_db)):
    """List all detected issues."""
    issues = db.query(Issue).order_by(Issue.detected_at.desc()).all()
    return issues


@router.get("/dataset/{dataset_id}", response_model=list[IssueResponse])
async def get_dataset_issues(dataset_id: str, db: Session = Depends(get_db)):
    """Get issues for a specific dataset."""
    issues = db.query(Issue).filter(
        Issue.dataset_id == dataset_id
    ).order_by(Issue.detected_at.desc()).all()
    return issues

"""
Profiles API router.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.dataset import DatasetProfile
from app.schemas.dataset import DatasetProfileResponse

router = APIRouter()


@router.get("/{dataset_id}", response_model=list[DatasetProfileResponse])
async def get_profiles(dataset_id: str, db: Session = Depends(get_db)):
    """Get all profiles for a dataset."""
    profiles = db.query(DatasetProfile).filter(
        DatasetProfile.dataset_id == dataset_id
    ).order_by(DatasetProfile.created_at.desc()).all()
    return profiles


@router.get("/{dataset_id}/latest", response_model=DatasetProfileResponse)
async def get_latest_profile(dataset_id: str, db: Session = Depends(get_db)):
    """Get latest profile for a dataset."""
    profile = db.query(DatasetProfile).filter(
        DatasetProfile.dataset_id == dataset_id
    ).order_by(DatasetProfile.created_at.desc()).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="No profile found")
    return profile

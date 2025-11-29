"""
Profiles API router.
Endpoints for viewing dataset profiles and statistics.
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/{dataset_id}")
async def get_profile(dataset_id: str):
    """Get profile for a dataset."""
    return {"profile": {}}

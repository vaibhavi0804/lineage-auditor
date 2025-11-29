"""
Datasets API router.
Endpoints for uploading, listing, and managing datasets.
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_datasets():
    """List all datasets."""
    return {"datasets": []}

@router.post("/upload")
async def upload_dataset():
    """Upload a new dataset."""
    return {"message": "Upload endpoint"}

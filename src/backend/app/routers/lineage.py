"""
Lineage API router.
Endpoints for dataset lineage graph queries.
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/{dataset_id}")
async def get_lineage(dataset_id: str):
    """Get lineage for a dataset."""
    return {"lineage": {}}

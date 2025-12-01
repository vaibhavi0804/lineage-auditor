# src/backend/app/routers/profiles.py
"""
Profiles API router.
"""
from fastapi import APIRouter, HTTPException
from app.supabase_client import table_select, table_insert
from app.schemas.dataset import DatasetProfileResponse
import uuid

# Adjust this if your table name differs
TABLE_PROFILES = "dataset_profiles"

router = APIRouter()


@router.get("/{dataset_id}", response_model=list[DatasetProfileResponse])
async def get_profiles(dataset_id: str):
    """Get all profiles for a dataset."""
    # select columns - include JSON fields as stored
    filters = f"dataset_id=eq.{dataset_id}"
    rows = await table_select(TABLE_PROFILES, columns="id,dataset_id,columns_metadata,statistics,sample_rows,created_at", filters=filters, params={"order":"created_at.desc"})
    return rows


@router.get("/{dataset_id}/latest", response_model=DatasetProfileResponse)
async def get_latest_profile(dataset_id: str):
    """Get latest profile for a dataset."""
    filters = f"dataset_id=eq.{dataset_id}"
    rows = await table_select(TABLE_PROFILES, columns="id,dataset_id,columns_metadata,statistics,sample_rows,created_at", filters=filters, params={"order":"created_at.desc", "limit":"1"})
    if not rows:
        raise HTTPException(status_code=404, detail="No profile found")
    return rows[0]


# If you had endpoints that create profiles, keep the logic but use table_insert:
async def create_profile(dataset_id: str, profile_payload: dict):
    """
    Helper to insert a dataset profile. Not an endpoint by itself.
    """
    payload = {
        "id": str(uuid.uuid4()),
        "dataset_id": dataset_id,
        "columns_metadata": profile_payload.get("columns_metadata"),
        "statistics": profile_payload.get("statistics"),
        "sample_rows": profile_payload.get("sample_rows"),
    }
    inserted = await table_insert(TABLE_PROFILES, payload)
    # table_insert returns a list when representation is returned
    return inserted[0] if isinstance(inserted, list) and inserted else inserted

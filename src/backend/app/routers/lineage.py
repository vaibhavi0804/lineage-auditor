# src/backend/app/routers/lineage.py
"""
Lineage API router.
"""
from fastapi import APIRouter
from app.supabase_client import table_select

# Adjust table name if different
TABLE_LINEAGE = "lineage"

router = APIRouter()


@router.get("/{dataset_id}")
async def get_lineage(dataset_id: str):
    """Get lineage (upstream and downstream) for a dataset."""
    # Upstream (sources): target_dataset_id == dataset_id
    upstream = await table_select(TABLE_LINEAGE, columns="source_dataset_id,job_name,job_type", filters=f"target_dataset_id=eq.{dataset_id}")
    # Downstream (targets): source_dataset_id == dataset_id
    downstream = await table_select(TABLE_LINEAGE, columns="target_dataset_id,job_name,job_type", filters=f"source_dataset_id=eq.{dataset_id}")

    return {
        "dataset_id": dataset_id,
        "upstream": [
            {
                "source_id": edge.get("source_dataset_id"),
                "job_name": edge.get("job_name"),
                "job_type": edge.get("job_type"),
            }
            for edge in upstream
        ],
        "downstream": [
            {
                "target_id": edge.get("target_dataset_id"),
                "job_name": edge.get("job_name"),
                "job_type": edge.get("job_type"),
            }
            for edge in downstream
        ],
    }

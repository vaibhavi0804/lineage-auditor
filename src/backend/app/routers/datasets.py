# src/backend/app/routers/datasets.py
"""
Datasets API router.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.supabase_client import table_select, table_insert
from app.schemas.dataset import DatasetCreate, DatasetResponse
import uuid
import logging
from io import BytesIO
import pandas as pd
from app.services.profiler import DatasetProfiler

logger = logging.getLogger(__name__)

# table name; change if your DB uses a different table name
TABLE_DATASETS = "datasets"

router = APIRouter()


@router.get("/", response_model=list[DatasetResponse])
async def list_datasets():
    """List all datasets."""
    rows = await table_select(TABLE_DATASETS, columns="id,name,row_count,column_count,storage_path,created_at")
    return rows


@router.post("/upload", response_model=DatasetResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    name: str | None = None,
):
    """Upload a CSV/Parquet dataset."""
    try:
        if name is None:
            name = file.filename

        # Read file into memory
        contents = await file.read()

        # Parse into DataFrame
        if file.filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(contents))
        elif file.filename.endswith(".parquet"):
            df = pd.read_parquet(BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Only CSV and Parquet supported")

        # Create dataset record (storage_path set later)
        dataset_id = str(uuid.uuid4())
        dataset_payload = {
            "id": dataset_id,
            "name": name,
            "row_count": len(df),
            "column_count": len(df.columns),
            "storage_path": None,
        }

        # Insert dataset row via Supabase
        inserted_dataset = await table_insert(TABLE_DATASETS, dataset_payload)
        # Supabase returns list representation
        created_dataset = inserted_dataset[0] if isinstance(inserted_dataset, list) and inserted_dataset else inserted_dataset

        # Try to upload to MinIO; fallback to local
        try:
            from app.utils.storage import upload_to_minio, save_local_file
            try:
                storage_path = upload_to_minio(dataset_id, file.filename, contents)
                logger.info("Uploaded to MinIO: %s", storage_path)
            except Exception as e_minio:
                # MinIO failed — save locally and log the error
                logger.warning("MinIO upload failed: %s. Saving local copy.", e_minio)
                storage_path = save_local_file(dataset_id, file.filename, contents)
                logger.info("Saved local fallback: %s", storage_path)

            # persist storage_path on dataset row via update
            # Supabase PATCH via table_update (not included here to keep small) — do a simple update call:
            try:
                # Update storage_path field
                from app.supabase_client import table_update
                updated = await table_update(
                    TABLE_DATASETS,
                    {"storage_path": storage_path},
                    filters=f"id=eq.{dataset_id}"
                )
                if isinstance(updated, list) and updated:
                    created_dataset = updated[0]
            except Exception as e_up:
                logger.warning("Failed to persist storage_path to dataset row: %s", e_up)

        except Exception as e_storage:
            # If even the fallback failed unexpectedly, log and continue profiling
            logger.error("Storage error (both MinIO and fallback): %s", e_storage)
            # We still proceed, dataset exists but storage_path is None

        # Profile it
        profile_data = DatasetProfiler.profile(df)
        # Create profile row using helper from profiles router (or call directly)
        from app.routers.profiles import create_profile
        try:
            created_profile = await create_profile(dataset_id, profile_data)
        except Exception as e_prof:
            logger.error("Profile creation failed: %s", e_prof)

        logger.info(f"Dataset {dataset_id} uploaded and profiled (storage_path={created_dataset.get('storage_path')})")
        # return dataset object in same shape as DatasetResponse expects
        return created_dataset

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(dataset_id: str):
    """
    Return dataset metadata by id.
    """
    row = await table_select(TABLE_DATASETS, columns="id,name,row_count,column_count,storage_path,created_at", filters=f"id=eq.{dataset_id}", params={"limit":"1"})
    if not row:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return row[0]

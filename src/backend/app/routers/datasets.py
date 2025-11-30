"""
Datasets API router.
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetCreate, DatasetResponse
import uuid
import logging
from io import BytesIO
import pandas as pd
from app.services.profiler import DatasetProfiler

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=list[DatasetResponse])
async def list_datasets(db: Session = Depends(get_db)):
    """List all datasets."""
    datasets = db.query(Dataset).all()
    return datasets


@router.post("/upload", response_model=DatasetResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = None,
    db: Session = Depends(get_db)
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
        dataset = Dataset(
            id=dataset_id,
            name=name,
            row_count=len(df),
            column_count=len(df.columns),
            storage_path=None,
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)

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

            # persist storage_path on dataset row
            dataset.storage_path = storage_path
            db.add(dataset)
            db.commit()
            db.refresh(dataset)

        except Exception as e_storage:
            # If even the fallback failed unexpectedly, log and continue profiling
            logger.error("Storage error (both MinIO and fallback): %s", e_storage)
            # We still proceed, dataset exists but storage_path is None

        # Profile it
        from app.models.dataset import DatasetProfile
        profile_data = DatasetProfiler.profile(df)
        profile = DatasetProfile(
            id=str(uuid.uuid4()),
            dataset_id=dataset_id,
            columns_metadata=profile_data["columns_metadata"],
            statistics=profile_data["statistics"],
            sample_rows=profile_data["sample_rows"],
        )
        db.add(profile)
        db.commit()

        logger.info(f"Dataset {dataset_id} uploaded and profiled (storage_path={dataset.storage_path})")
        return dataset

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(dataset_id: str, db: Session = Depends(get_db)):
    """
    Return dataset metadata by id.
    """
    ds = db.query(Dataset).filter(Dataset.id == dataset_id).one_or_none()
    if ds is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return ds
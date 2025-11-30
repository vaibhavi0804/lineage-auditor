# src/backend/app/utils/storage.py
from pathlib import Path
import io
from typing import Optional
import logging

from minio import Minio
from minio.error import S3Error

from app.config import settings

logger = logging.getLogger(__name__)

# Local fallback directory (keeps a copy if MinIO is not available)
ROOT = Path.cwd()
LOCAL_UPLOAD_DIR = ROOT / "storage" / "uploads"
LOCAL_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _safe_name(filename: str) -> str:
    return filename.replace("/", "_").replace("..", "_")


def upload_to_minio(dataset_id: str, filename: str, content: bytes) -> str:
    """
    Upload content to MinIO and return object path string (minio://bucket/object).
    Raises exception on failure.
    """
    endpoint = settings.MINIO_ENDPOINT
    access_key = settings.MINIO_ACCESS_KEY
    secret_key = settings.MINIO_SECRET_KEY
    bucket = settings.MINIO_BUCKET

    # Minio expects host:port (no scheme) for endpoint in Minio() constructor
    client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=settings.MINIO_USE_SSL)

    # Ensure bucket exists
    try:
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
    except Exception as e:
        logger.warning("MinIO bucket check/create failed: %s", e)
        raise

    safe_name = _safe_name(filename)
    object_name = f"uploads/{dataset_id}-{safe_name}"

    try:
        # put_object expects a stream; use io.BytesIO
        client.put_object(bucket, object_name, data=io.BytesIO(content), length=len(content))
    except S3Error as e:
        logger.error("MinIO put_object failed: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected MinIO error: %s", e)
        raise

    return f"minio://{bucket}/{object_name}"


def save_local_file(dataset_id: str, filename: str, content: bytes) -> str:
    """
    Save a local copy (fallback) and return relative path.
    """
    safe = _safe_name(filename)
    out_name = f"{dataset_id}-{safe}"
    out_path = LOCAL_UPLOAD_DIR / out_name
    out_path.write_bytes(content)
    # return relative path for readability
    return str(out_path.relative_to(Path.cwd()))

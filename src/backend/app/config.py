"""
Application configuration.
Loads from environment variables or defaults.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App settings."""
    
    # API
    API_TITLE: str = "Lineage Auditor API"
    API_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/lineage_auditor"
    )
    
    # MinIO
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_BUCKET: str = os.getenv("MINIO_BUCKET", "datasets")
    MINIO_USE_SSL: bool = os.getenv("MINIO_USE_SSL", "False").lower() == "true"
    
    # Airflow (for lineage extraction)
    AIRFLOW_HOME: str = os.getenv("AIRFLOW_HOME", "/opt/airflow")
    AIRFLOW_DAGS_FOLDER: str = os.getenv(
        "AIRFLOW_DAGS_FOLDER",
        "/opt/airflow/dags"
    )

    # Frontend dev URL (optional; present in .env from frontend tooling)
    VITE_API_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

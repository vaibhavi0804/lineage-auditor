"""
Application configuration.
Loads from environment variables or defaults.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App settings."""
    
    # API
    API_TITLE: str = "Lineage Auditor API"
    API_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/lineage_auditor"
    )
    
    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "datasets"
    MINIO_USE_SSL: bool = False
    
    # Airflow (for lineage extraction)

    AIRFLOW_HOME: str = "/opt/airflow"
    AIRFLOW_DAGS_FOLDER: str = "/opt/airflow/dags"

    VITE_API_URL: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


# lazy settings factory (avoids import-time failures)
_settings_instance = None

def get_settings() -> Settings:
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance

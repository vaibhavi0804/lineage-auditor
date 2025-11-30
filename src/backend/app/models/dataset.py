"""
Database models for datasets, profiles, issues, and lineage.
"""
from sqlalchemy import Column, String, DateTime, Integer, Float, JSON, Boolean, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class Dataset(Base):
    """Dataset table – stores dataset metadata."""
    __tablename__ = "datasets"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    row_count = Column(Integer)
    column_count = Column(Integer)
    storage_path = Column(String)  # Path in MinIO
    
    # Relationships
    profiles = relationship("DatasetProfile", back_populates="dataset", cascade="all, delete-orphan")
    issues = relationship("Issue", back_populates="dataset", cascade="all, delete-orphan")
    lineage_sources = relationship("Lineage", foreign_keys="Lineage.target_dataset_id", back_populates="target")
    lineage_targets = relationship("Lineage", foreign_keys="Lineage.source_dataset_id", back_populates="source")


class DatasetProfile(Base):
    """Dataset profile – stores statistics for a dataset snapshot."""
    __tablename__ = "dataset_profiles"
    
    id = Column(String, primary_key=True, index=True)
    dataset_id = Column(String, ForeignKey("datasets.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    columns_metadata = Column(JSON)  # { "col_name": { "dtype": "int", "null_count": 10, ... } }
    statistics = Column(JSON)  # { "col_name": { "mean": 5.2, "std": 1.1, ... } }
    sample_rows = Column(JSON)  # First N rows for inspection
    
    dataset = relationship("Dataset", back_populates="profiles")


class IssueType(str, enum.Enum):
    """Types of issues detected."""
    SCHEMA_CHANGE = "schema_change"
    DISTRIBUTION_DRIFT = "distribution_drift"
    SEMANTIC_DRIFT = "semantic_drift"
    NULL_SPIKE = "null_spike"
    CARDINALITY_ANOMALY = "cardinality_anomaly"
    LABEL_FLIP = "label_flip"


class IssueSeverity(str, enum.Enum):
    """Severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Issue(Base):
    """Issue table – detected data quality issues."""
    __tablename__ = "issues"
    
    id = Column(String, primary_key=True, index=True)
    dataset_id = Column(String, ForeignKey("datasets.id"), nullable=False)
    issue_type = Column(Enum(IssueType), nullable=False)
    severity = Column(Enum(IssueSeverity), nullable=False)
    column_name = Column(String)
    description = Column(Text)
    evidence = Column(JSON)  # { "before": {...}, "after": {...}, "p_value": 0.001 }
    detected_at = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text)
    
    dataset = relationship("Dataset", back_populates="issues")


class Lineage(Base):
    """Lineage table – tracks dataset dependencies."""
    __tablename__ = "lineage"
    
    id = Column(String, primary_key=True, index=True)
    source_dataset_id = Column(String, ForeignKey("datasets.id"), nullable=False)
    target_dataset_id = Column(String, ForeignKey("datasets.id"), nullable=False)
    job_name = Column(String)  # Name of the job that produced target from source
    job_type = Column(String)  # "join", "aggregate", "filter", "transform", etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    confidence = Column(Float, default=1.0)  # 0-1 confidence score
    
    source = relationship("Dataset", foreign_keys=[source_dataset_id], back_populates="lineage_targets")
    target = relationship("Dataset", foreign_keys=[target_dataset_id], back_populates="lineage_sources")

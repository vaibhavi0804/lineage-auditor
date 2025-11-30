"""
Lineage API router.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.dataset import Lineage

router = APIRouter()


@router.get("/{dataset_id}")
async def get_lineage(dataset_id: str, db: Session = Depends(get_db)):
    """Get lineage (upstream and downstream) for a dataset."""
    # Upstream (sources)
    upstream = db.query(Lineage).filter(
        Lineage.target_dataset_id == dataset_id
    ).all()
    
    # Downstream (targets)
    downstream = db.query(Lineage).filter(
        Lineage.source_dataset_id == dataset_id
    ).all()
    
    return {
        "dataset_id": dataset_id,
        "upstream": [
            {
                "source_id": edge.source_dataset_id,
                "job_name": edge.job_name,
                "job_type": edge.job_type,
            }
            for edge in upstream
        ],
        "downstream": [
            {
                "target_id": edge.target_dataset_id,
                "job_name": edge.job_name,
                "job_type": edge.job_type,
            }
            for edge in downstream
        ],
    }

"""
Dataset profiler – extracts statistics from datasets.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class DatasetProfiler:
    """Profiles a dataset to extract statistics."""
    
    @staticmethod
    def profile(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Profile a DataFrame.
        
        Returns:
            {
                "columns_metadata": { "col": { "dtype": "int64", "null_count": 5, ... } },
                "statistics": { "col": { "mean": 5.2, "std": 1.1, "min": 0, "max": 10 } },
                "sample_rows": [first 5 rows as dicts]
            }
        """
        try:
            columns_metadata = {}
            statistics = {}
            
            for col in df.columns:
                # Metadata
                columns_metadata[col] = {
                    "dtype": str(df[col].dtype),
                    "null_count": int(df[col].isnull().sum()),
                    "null_percentage": float(df[col].isnull().sum() / len(df) * 100),
                    "cardinality": int(df[col].nunique()),
                }
                
                # Statistics (numeric only)
                if pd.api.types.is_numeric_dtype(df[col]):
                    statistics[col] = {
                        "mean": float(df[col].mean()) if not df[col].isna().all() else None,
                        "std": float(df[col].std()) if not df[col].isna().all() else None,
                        "min": float(df[col].min()) if not df[col].isna().all() else None,
                        "max": float(df[col].max()) if not df[col].isna().all() else None,
                        "median": float(df[col].median()) if not df[col].isna().all() else None,
                    }
            
            return {
                "columns_metadata": columns_metadata,
                "statistics": statistics,
                "sample_rows": df.head(10).to_dict(orient="records"),
            }
        except Exception as e:
            logger.error(f"Profiling error: {e}")
            raise

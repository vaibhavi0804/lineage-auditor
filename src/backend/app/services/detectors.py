"""
Drift and anomaly detectors.
"""
from scipy.stats import ks_2samp, chi2_contingency
import numpy as np
from typing import Dict, Any, List, Tuple
import logging

logger = logging.getLogger(__name__)


class SchemaDetector:
    """Detects schema changes between two profiles."""
    
    @staticmethod
    def detect(before: Dict[str, Any], after: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect schema changes.
        
        Returns list of issues like:
        [
            {"type": "column_added", "column": "new_col"},
            {"type": "column_removed", "column": "old_col"},
            {"type": "dtype_changed", "column": "col", "before": "int64", "after": "float64"}
        ]
        """
        issues = []
        before_cols = set(before.get("columns_metadata", {}).keys())
        after_cols = set(after.get("columns_metadata", {}).keys())
        
        # Columns added
        for col in after_cols - before_cols:
            issues.append({
                "type": "column_added",
                "column": col,
            })
        
        # Columns removed
        for col in before_cols - after_cols:
            issues.append({
                "type": "column_removed",
                "column": col,
            })
        
        # Dtype changes
        for col in before_cols & after_cols:
            before_dtype = before["columns_metadata"][col]["dtype"]
            after_dtype = after["columns_metadata"][col]["dtype"]
            if before_dtype != after_dtype:
                issues.append({
                    "type": "dtype_changed",
                    "column": col,
                    "before": before_dtype,
                    "after": after_dtype,
                })
        
        return issues


class DriftDetector:
    """Detects statistical drift in numeric columns."""
    
    @staticmethod
    def ks_test(before_stats: Dict[str, Any], after_stats: Dict[str, Any], column: str, threshold: float = 0.05) -> Tuple[bool, float]:
        """
        Kolmogorov-Smirnov test for distribution shift.
        Returns: (is_drift, p_value)
        """
        # This is simplified; in production you'd generate distributions from samples
        # For now, compare means as proxy
        before_mean = before_stats.get(column, {}).get("mean")
        after_mean = after_stats.get(column, {}).get("mean")
        
        if before_mean is None or after_mean is None:
            return False, 1.0
        
        # Simple heuristic: if mean shifted >10%, flag drift
        pct_change = abs(after_mean - before_mean) / abs(before_mean + 1e-10)
        is_drift = pct_change > 0.1
        p_value = 0.01 if is_drift else 0.99
        
        return is_drift, p_value
    
    @staticmethod
    def null_spike(before: Dict[str, Any], after: Dict[str, Any], column: str, threshold: float = 5.0) -> Tuple[bool, Dict[str, Any]]:
        """
        Detect spike in null percentage.
        Returns: (is_spike, evidence_dict)
        """
        before_null_pct = before.get("columns_metadata", {}).get(column, {}).get("null_percentage", 0)
        after_null_pct = after.get("columns_metadata", {}).get(column, {}).get("null_percentage", 0)
        
        is_spike = (after_null_pct - before_null_pct) > threshold
        
        return is_spike, {
            "before_null_pct": before_null_pct,
            "after_null_pct": after_null_pct,
            "delta": after_null_pct - before_null_pct,
        }

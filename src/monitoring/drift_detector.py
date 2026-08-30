"""
Model Drift & Data Quality Monitoring Engine.

Calculates Population Stability Index (PSI), Kolmogorov-Smirnov (KS) statistics on feature distributions,
missingness ratios, prediction quality classification (GOOD, LIMITED, INSUFFICIENT), and prediction distribution drift.
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

def calculate_psi(baseline_values: np.ndarray, target_values: np.ndarray, num_buckets: int = 10) -> float:
    """
    Computes Population Stability Index (PSI) between baseline and incoming feature distributions.
    """
    if len(baseline_values) == 0 or len(target_values) == 0:
        return 0.0
        
    percentiles = np.linspace(0, 100, num_buckets + 1)
    buckets = np.percentile(baseline_values, percentiles)
    buckets[0] -= 1e-5
    buckets[-1] += 1e-5
    
    baseline_counts, _ = np.histogram(baseline_values, bins=buckets)
    target_counts, _ = np.histogram(target_values, bins=buckets)
    
    baseline_pct = baseline_counts / len(baseline_values)
    target_pct = target_counts / len(target_values)
    
    # Smooth zero probabilities
    baseline_pct = np.where(baseline_pct == 0, 1e-4, baseline_pct)
    target_pct = np.where(target_pct == 0, 1e-4, target_pct)
    
    psi_value = np.sum((target_pct - baseline_pct) * np.log(target_pct / baseline_pct))
    return round(float(psi_value), 4)

def evaluate_data_quality_and_drift(
    baseline_df: pd.DataFrame,
    current_df: pd.DataFrame
) -> Dict[str, Any]:
    """
    Evaluates data quality rating and feature distribution drift.
    """
    # 1. Missingness Score
    missing_ratio = float(current_df.isnull().sum().sum()) / max(current_df.size, 1)
    
    if missing_ratio > 0.40 or len(current_df) < 3:
        data_quality = "INSUFFICIENT"
    elif missing_ratio > 0.15:
        data_quality = "LIMITED"
    else:
        data_quality = "GOOD"
        
    # 2. Feature Drift (PSI & KS Test)
    drift_metrics = {}
    numerical_cols = [c for c in current_df.columns if pd.api.types.is_numeric_dtype(current_df[c]) and c not in ["patient_id", "target_deterioration"]]
    
    for col in numerical_cols[:5]:
        base_vals = baseline_df[col].dropna().values
        curr_vals = current_df[col].dropna().values
        
        if len(base_vals) > 5 and len(curr_vals) > 5:
            psi_val = calculate_psi(base_vals, curr_vals)
            ks_stat, p_val = ks_2samp(base_vals, curr_vals)
            drift_status = "SIGNIFICANT_DRIFT" if psi_val > 0.25 else ("MODERATE_DRIFT" if psi_val > 0.10 else "STABLE")
            
            drift_metrics[col] = {
                "psi": psi_val,
                "ks_statistic": round(float(ks_stat), 4),
                "p_value": round(float(p_val), 4),
                "drift_status": drift_status
            }
            
    return {
        "data_quality_rating": data_quality,
        "missingness_ratio_pct": round(missing_ratio * 100.0, 1),
        "total_observations_evaluated": len(current_df),
        "feature_drift_summary": drift_metrics,
        "disclaimer": "Research model monitoring statistics for data quality & population stability index tracking."
    }

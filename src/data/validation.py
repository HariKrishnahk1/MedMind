"""
Data Validation Module for Clinical Deterioration Prediction Engine.

Enforces schema integrity, timestamp order, value range bounds, and input sanity checks.
"""

from typing import Tuple, List, Dict, Any
import numpy as np
import pandas as pd

REQUIRED_INPUT_COLUMNS = [
    "patient_id",
    "timestamp",
    "age",
    "sex",
    "heart_rate",
    "systolic_bp",
    "diastolic_bp",
    "spo2",
    "respiratory_rate",
    "temperature",
    "lab_value_1",
    "lab_value_2",
    "diagnosis_category",
    "medication_category"
]

CLINICAL_BOUNDS = {
    "age": (0, 120),
    "heart_rate": (20, 250),
    "systolic_bp": (40, 300),
    "diastolic_bp": (20, 200),
    "spo2": (50, 100),
    "respiratory_rate": (4, 60),
    "temperature": (30.0, 45.0),
    "lab_value_1": (0.0, 30.0),
    "lab_value_2": (0.0, 20.0)
}

def validate_raw_schema(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validates that input dataframe has all required columns and valid non-empty structure.
    """
    errors = []
    if df is None or df.empty:
        return False, ["Input DataFrame is empty or None."]
        
    missing_cols = [col for col in REQUIRED_INPUT_COLUMNS if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
        
    return len(errors) == 0, errors

def validate_clinical_ranges(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """
    Checks clinical numerical values against plausible range bounds and replaces extreme outliers with NaN.
    """
    warnings = []
    df_clean = df.copy()
    
    for col, (min_val, max_val) in CLINICAL_BOUNDS.items():
        if col in df_clean.columns:
            invalid_mask = (df_clean[col] < min_val) | (df_clean[col] > max_val)
            invalid_count = int(invalid_mask.sum())
            if invalid_count > 0:
                warnings.append(f"Column '{col}' has {invalid_count} values outside [{min_val}, {max_val}]. Setting them to NaN.")
                df_clean.loc[invalid_mask, col] = np.nan
                
    return df_clean, warnings

def validate_and_clean_dataset(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Full validation and cleaning pipeline for raw observation data.
    
    - Validates schema
    - Converts timestamps
    - Sorts by patient_id and timestamp
    - Removes duplicate (patient_id, timestamp) rows keeping latest
    - Filters out-of-range clinical anomalies
    """
    report = {"errors": [], "warnings": [], "initial_rows": len(df), "final_rows": 0}
    
    # 1. Validate Schema
    valid_schema, schema_errors = validate_raw_schema(df)
    if not valid_schema:
        report["errors"].extend(schema_errors)
        raise ValueError(f"Schema validation failed: {schema_errors}")
        
    df_clean = df.copy()
    
    # 2. Datetime Conversion
    try:
        df_clean["timestamp"] = pd.to_datetime(df_clean["timestamp"])
    except Exception as e:
        report["errors"].append(f"Timestamp conversion error: {str(e)}")
        raise ValueError(f"Invalid timestamp format: {str(e)}")
        
    # 3. Sort by patient_id and timestamp
    df_clean = df_clean.sort_values(by=["patient_id", "timestamp"]).reset_index(drop=True)
    
    # 4. Check & Remove Duplicates
    dup_mask = df_clean.duplicated(subset=["patient_id", "timestamp"], keep="last")
    dup_count = int(dup_mask.sum())
    if dup_count > 0:
        report["warnings"].append(f"Found and removed {dup_count} duplicate patient-timestamp observations.")
        df_clean = df_clean[~dup_mask].reset_index(drop=True)
        
    # 5. Range validation
    df_clean, range_warnings = validate_clinical_ranges(df_clean)
    report["warnings"].extend(range_warnings)
    
    report["final_rows"] = len(df_clean)
    return df_clean, report

"""
Preprocessing and Temporal Target Generation Pipeline.

Handles:
- Temporal target creation (target_deterioration) without data leakage
- Feature selection & encoding
- Missing value imputation
- Scaling and train/test dataset preparation
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import joblib
import numpy as np
import pandas as pd
from typing import Tuple, List, Dict, Any
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from src.data.validation import validate_and_clean_dataset
from src.features.clinical_features import generate_all_clinical_features, NUMERICAL_CLINICAL_VARS

def compute_temporal_deterioration_target(
    df: pd.DataFrame,
    prediction_horizon_minutes: int = 60
) -> pd.DataFrame:
    """
    Constructs the synthetic near-term deterioration target variable (`target_deterioration`).
    
    Definition:
    For observation at timestamp T, target = 1 if ANY observation for the same patient in the
    future window (T, T + horizon_minutes] exhibits acute clinical deterioration:
    - heart_rate > 120 or heart_rate < 45
    - systolic_bp < 90 or systolic_bp > 180
    - spo2 < 90
    - respiratory_rate > 30 or respiratory_rate < 8
    - lab_value_1 (Lactate) > 3.5
    
    Data Leakage Prevention Guarantee:
    - Target construction reads ONLY future timestamps (T, T + horizon].
    - Model input features read ONLY historical timestamps <= T.
    - Future vitals are never used as model inputs.
    
    Parameters:
    -----------
    df: DataFrame containing patient observations with timestamps.
    prediction_horizon_minutes: Lookahead window in minutes.
    
    Returns:
    --------
    pd.DataFrame with added `target_deterioration` column.
    """
    df_sorted = df.sort_values(by=["patient_id", "timestamp"]).reset_index(drop=True)
    df_sorted["timestamp"] = pd.to_datetime(df_sorted["timestamp"])
    
    targets = np.zeros(len(df_sorted), dtype=int)
    
    for pid, group in df_sorted.groupby("patient_id", sort=False):
        indices = group.index.values
        timestamps = group["timestamp"].values
        hrs = group["heart_rate"].values
        sbps = group["systolic_bp"].values
        spo2s = group["spo2"].values
        rrs = group["respiratory_rate"].values
        lab1s = group["lab_value_1"].values
        
        n = len(group)
        for i in range(n):
            t_current = timestamps[i]
            t_max = t_current + np.timedelta64(prediction_horizon_minutes, 'm')
            
            # Find future observations within prediction window (t_current, t_max]
            future_mask = (timestamps > t_current) & (timestamps <= t_max)
            
            if np.any(future_mask):
                f_hrs = hrs[future_mask]
                f_sbps = sbps[future_mask]
                f_spo2s = spo2s[future_mask]
                f_rrs = rrs[future_mask]
                f_lab1s = lab1s[future_mask]
                
                # Compute multi-factor synthetic latent deterioration score
                # 1. Single extreme threshold breach
                det_hr = np.any((f_hrs > 120) | (f_hrs < 45))
                det_sbp = np.any((f_sbps < 90) | (f_sbps > 180))
                det_spo2 = np.any((f_spo2s < 90) & ~np.isnan(f_spo2s))
                det_rr = np.any(((f_rrs > 30) | (f_rrs < 8)) & ~np.isnan(f_rrs))
                det_lab1 = np.any((f_lab1s > 3.5) & ~np.isnan(f_lab1s))
                
                # 2. Combined multi-vital trajectory deviation (latent score > 2.0)
                hr_dev = np.nanmax(np.abs(f_hrs - 75.0)) / 25.0
                spo2_dev = np.nanmax(np.maximum(98.0 - f_spo2s, 0.0)) / 5.0 if not np.all(np.isnan(f_spo2s)) else 0.0
                sbp_dev = np.nanmax(np.abs(f_sbps - 120.0)) / 30.0
                latent_score = hr_dev + spo2_dev + sbp_dev
                
                if det_hr or det_sbp or det_spo2 or det_rr or det_lab1 or (latent_score >= 2.0):
                    targets[indices[i]] = 1
            else:
                targets[indices[i]] = 0
                
    df_sorted["target_deterioration"] = targets
    return df_sorted


def get_feature_columns(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """
    Identifies numerical and categorical feature column names for model training.
    """
    exclude_cols = {"patient_id", "timestamp", "target_deterioration"}
    
    categorical_cols = ["sex", "diagnosis_category", "medication_category"]
    
    numerical_cols = [
        col for col in df.columns 
        if col not in exclude_cols and col not in categorical_cols and pd.api.types.is_numeric_dtype(df[col])
    ]
    
    return numerical_cols, categorical_cols

def build_preprocessing_pipeline(
    numerical_cols: List[str],
    categorical_cols: List[str]
) -> ColumnTransformer:
    """
    Creates Scikit-learn ColumnTransformer pipeline for median imputation, standard scaling, and one-hot encoding.
    """
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_pipeline, numerical_cols),
            ('cat', cat_pipeline, categorical_cols)
        ]
    )
    
    return preprocessor

def run_preprocessing_pipeline(
    raw_data_path: str = "data/raw/synthetic_clinical_data.csv",
    output_processed_path: str = "data/processed/model_dataset.csv",
    horizon_minutes: int = 60
) -> pd.DataFrame:
    """
    Executes full data loading, validation, feature engineering, and temporal target creation pipeline.
    Saves processed dataset to `data/processed/model_dataset.csv`.
    """
    print(f"Loading raw dataset from {raw_data_path}...")
    raw_df = pd.read_csv(raw_data_path)
    
    print("Validating raw data schema and range bounds...")
    cleaned_df, report = validate_and_clean_dataset(raw_df)
    print(f"Validation complete. Rows: {report['initial_rows']} -> {report['final_rows']}. Warnings: {len(report['warnings'])}")
    
    print("Generating baseline, trend, and trajectory features...")
    featured_df = generate_all_clinical_features(cleaned_df)
    
    print(f"Computing temporal deterioration target (horizon: {horizon_minutes} mins)...")
    final_df = compute_temporal_deterioration_target(featured_df, prediction_horizon_minutes=horizon_minutes)
    
    target_count = final_df['target_deterioration'].sum()
    total_count = len(final_df)
    print(f"Target distribution: Positive = {target_count} ({target_count/total_count:.2%}), Negative = {total_count - target_count}")
    
    os.makedirs(os.path.dirname(output_processed_path), exist_ok=True)
    final_df.to_csv(output_processed_path, index=False)
    print(f"Processed model dataset saved to {output_processed_path}")
    
    return final_df

if __name__ == "__main__":
    run_preprocessing_pipeline()

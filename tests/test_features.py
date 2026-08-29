"""
Unit tests for clinical trend and patient-specific baseline feature engineering.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import pandas as pd
import numpy as np

from src.features.clinical_features import compute_patient_level_features, generate_all_clinical_features

def test_compute_patient_level_features():
    df_patient = pd.DataFrame([
        {
            "patient_id": "P001", "timestamp": "2026-01-01 08:00:00",
            "heart_rate": 70.0, "systolic_bp": 120.0, "diastolic_bp": 75.0,
            "spo2": 98.0, "respiratory_rate": 16.0, "temperature": 36.8,
            "lab_value_1": 1.0, "lab_value_2": 0.8,
            "diagnosis_category": "Cardiac", "medication_category": "None"
        },
        {
            "patient_id": "P001", "timestamp": "2026-01-01 09:00:00",
            "heart_rate": 90.0, "systolic_bp": 110.0, "diastolic_bp": 70.0,
            "spo2": 95.0, "respiratory_rate": 20.0, "temperature": 37.2,
            "lab_value_1": 1.5, "lab_value_2": 0.9,
            "diagnosis_category": "Cardiac", "medication_category": "Oxygen"
        }
    ])
    
    feat_df = compute_patient_level_features(df_patient)
    
    # Verify generated baseline & trend features
    assert "heart_rate_current" in feat_df.columns
    assert "heart_rate_previous" in feat_df.columns
    assert "heart_rate_change_from_previous" in feat_df.columns
    assert "heart_rate_change_from_baseline" in feat_df.columns
    assert "heart_rate_trend_slope" in feat_df.columns
    assert "time_since_last_obs_mins" in feat_df.columns
    
    # Check values for observation 2 (index 1)
    assert feat_df["heart_rate_current"].iloc[1] == 90.0
    assert feat_df["heart_rate_previous"].iloc[1] == 70.0
    assert feat_df["heart_rate_change_from_previous"].iloc[1] == 20.0
    assert feat_df["time_since_last_obs_mins"].iloc[1] == 60.0

def test_no_future_leakage_in_features():
    """Verify that features for row i depend ONLY on rows 0..i"""
    df_patient = pd.DataFrame([
        {
            "patient_id": "P001", "timestamp": "2026-01-01 08:00:00",
            "heart_rate": 70.0, "systolic_bp": 120.0, "diastolic_bp": 75.0,
            "spo2": 98.0, "respiratory_rate": 16.0, "temperature": 36.8,
            "lab_value_1": 1.0, "lab_value_2": 0.8,
            "diagnosis_category": "Cardiac", "medication_category": "None"
        },
        {
            "patient_id": "P001", "timestamp": "2026-01-01 09:00:00",
            "heart_rate": 90.0, "systolic_bp": 110.0, "diastolic_bp": 70.0,
            "spo2": 95.0, "respiratory_rate": 20.0, "temperature": 37.2,
            "lab_value_1": 1.5, "lab_value_2": 0.9,
            "diagnosis_category": "Cardiac", "medication_category": "Oxygen"
        }
    ])
    
    # Compute features for 1 row vs 2 rows
    feat_df1 = compute_patient_level_features(df_patient.head(1))
    feat_df2 = compute_patient_level_features(df_patient)
    
    # Row 0 feature values must be EXACTLY identical regardless of row 1 existing
    assert feat_df1["heart_rate_recent_mean"].iloc[0] == feat_df2["heart_rate_recent_mean"].iloc[0]
    assert feat_df1["heart_rate_change_from_baseline"].iloc[0] == feat_df2["heart_rate_change_from_baseline"].iloc[0]

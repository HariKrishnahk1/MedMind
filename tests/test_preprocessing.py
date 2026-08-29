"""
Unit tests for data preprocessing module and temporal target creation.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import pandas as pd
import numpy as np

from src.data.preprocessing import compute_temporal_deterioration_target, get_feature_columns

def test_compute_temporal_deterioration_target():
    # Patient with stable initial observation at T1, but severe deterioration at T2 (within 60 mins)
    df = pd.DataFrame([
        {
            "patient_id": "P001", "timestamp": "2026-01-01 12:00:00",
            "heart_rate": 75.0, "systolic_bp": 120.0, "spo2": 98.0,
            "respiratory_rate": 16.0, "lab_value_1": 1.0
        },
        {
            "patient_id": "P001", "timestamp": "2026-01-01 12:30:00",  # Future window T1 -> T2
            "heart_rate": 135.0, "systolic_bp": 85.0, "spo2": 88.0,    # Deteriorated!
            "respiratory_rate": 32.0, "lab_value_1": 4.5
        }
    ])
    
    target_df = compute_temporal_deterioration_target(df, prediction_horizon_minutes=60)
    assert "target_deterioration" in target_df.columns
    # T1 target should be 1 because T2 within 60 mins deteriorates
    assert target_df["target_deterioration"].iloc[0] == 1

def test_get_feature_columns():
    df = pd.DataFrame({
        "patient_id": ["P001"],
        "timestamp": ["2026-01-01 12:00:00"],
        "target_deterioration": [0],
        "heart_rate_current": [80.0],
        "sex": ["M"],
        "diagnosis_category": ["Sepsis"]
    })
    num_cols, cat_cols = get_feature_columns(df)
    assert "heart_rate_current" in num_cols
    assert "sex" in cat_cols
    assert "patient_id" not in num_cols
    assert "target_deterioration" not in num_cols

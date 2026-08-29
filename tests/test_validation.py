"""
Unit tests for data validation module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import pandas as pd
import numpy as np

from src.data.validation import (
    validate_raw_schema,
    validate_clinical_ranges,
    validate_and_clean_dataset
)

def test_validate_raw_schema_valid():
    df = pd.DataFrame([{
        "patient_id": "P001", "timestamp": "2026-01-01 12:00:00",
        "age": 50, "sex": "M", "heart_rate": 80, "systolic_bp": 120,
        "diastolic_bp": 80, "spo2": 98, "respiratory_rate": 16,
        "temperature": 37.0, "lab_value_1": 1.0, "lab_value_2": 0.8,
        "diagnosis_category": "Cardiac", "medication_category": "None"
    }])
    valid, errors = validate_raw_schema(df)
    assert valid is True
    assert len(errors) == 0

def test_validate_raw_schema_missing_column():
    df = pd.DataFrame([{"patient_id": "P001", "age": 50}])
    valid, errors = validate_raw_schema(df)
    assert valid is False
    assert len(errors) > 0

def test_validate_clinical_ranges_outliers():
    df = pd.DataFrame([{
        "age": 50, "heart_rate": 300, "systolic_bp": 120,
        "diastolic_bp": 80, "spo2": 98, "respiratory_rate": 16,
        "temperature": 37.0, "lab_value_1": 1.0, "lab_value_2": 0.8
    }])
    df_clean, warnings = validate_clinical_ranges(df)
    assert np.isnan(df_clean["heart_rate"].iloc[0])
    assert len(warnings) > 0

def test_validate_and_clean_dataset_duplicates():
    df = pd.DataFrame([
        {
            "patient_id": "P001", "timestamp": "2026-01-01 12:00:00",
            "age": 50, "sex": "M", "heart_rate": 80, "systolic_bp": 120,
            "diastolic_bp": 80, "spo2": 98, "respiratory_rate": 16,
            "temperature": 37.0, "lab_value_1": 1.0, "lab_value_2": 0.8,
            "diagnosis_category": "Cardiac", "medication_category": "None"
        },
        {
            "patient_id": "P001", "timestamp": "2026-01-01 12:00:00",  # Duplicate timestamp
            "age": 50, "sex": "M", "heart_rate": 85, "systolic_bp": 120,
            "diastolic_bp": 80, "spo2": 98, "respiratory_rate": 16,
            "temperature": 37.0, "lab_value_1": 1.0, "lab_value_2": 0.8,
            "diagnosis_category": "Cardiac", "medication_category": "None"
        }
    ])
    cleaned_df, report = validate_and_clean_dataset(df)
    assert len(cleaned_df) == 1
    assert cleaned_df["heart_rate"].iloc[0] == 85

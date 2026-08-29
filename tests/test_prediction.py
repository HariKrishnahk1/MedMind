"""
Integration tests for DeteriorationPredictor and FastAPI Prediction Service.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import pandas as pd
from fastapi.testclient import TestClient

from src.models.predict import DeteriorationPredictor
from src.service.app import app

def test_deterioration_predictor_end_to_end():
    predictor = DeteriorationPredictor()
    
    sample_obs = [
        {
            "patient_id": "P_TEST_01", "timestamp": "2026-01-01 08:00:00",
            "age": 60, "sex": "F", "heart_rate": 75.0, "systolic_bp": 120.0,
            "diastolic_bp": 75.0, "spo2": 98.0, "respiratory_rate": 16.0,
            "temperature": 36.8, "lab_value_1": 1.0, "lab_value_2": 0.8,
            "diagnosis_category": "Cardiac", "medication_category": "None"
        },
        {
            "patient_id": "P_TEST_01", "timestamp": "2026-01-01 09:00:00",
            "age": 60, "sex": "F", "heart_rate": 115.0, "systolic_bp": 92.0,
            "diastolic_bp": 60.0, "spo2": 91.0, "respiratory_rate": 24.0,
            "temperature": 38.2, "lab_value_1": 3.2, "lab_value_2": 1.4,
            "diagnosis_category": "Cardiac", "medication_category": "Oxygen"
        }
    ]
    
    result = predictor.predict(sample_obs, horizon_minutes=15)
    
    assert result["patient_id"] == "P_TEST_01"
    assert 0.0 <= result["risk_score"] <= 1.0
    assert result["risk_level"] in ["low", "medium", "high"]
    assert result["prediction_horizon_minutes"] == 15
    assert isinstance(result["explanation"], list)

def test_fastapi_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_fastapi_predict_endpoint():
    client = TestClient(app)
    payload = {
        "prediction_horizon_minutes": 15,
        "observations": [
            {
                "patient_id": "P_TEST_02", "timestamp": "2026-01-01 08:00:00",
                "age": 72, "sex": "M", "heart_rate": 82.0, "systolic_bp": 118.0,
                "diastolic_bp": 76.0, "spo2": 97.0, "respiratory_rate": 18.0,
                "temperature": 37.0, "lab_value_1": 1.2, "lab_value_2": 0.9,
                "diagnosis_category": "Sepsis", "medication_category": "None"
            }
        ]
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["patient_id"] == "P_TEST_02"
    assert "risk_score" in data
    assert "risk_level" in data
    assert "explanation" in data
    assert "disclaimer" in data

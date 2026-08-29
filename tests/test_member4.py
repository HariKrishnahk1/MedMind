import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient

from src.service.app import app
from src.service.db import mock_patients, mock_alerts, mock_timelines

def test_member4_end_to_end_workflow():
    client = TestClient(app)
    
    # Setup test patient P001 in db
    p001 = {
        "id": "P001",
        "name": "Test Patient",
        "age": 60,
        "gender": "F",
        "mrn": "MRN-001",
        "priority": "Stable",
        "primaryDiagnosis": "Testing",
        "vitals": {}
    }
    mock_patients.append(p001)
    
    # 1. Predict deterioration to trigger Priority update and Alerts
    payload = {
        "prediction_horizon_minutes": 15,
        "observations": [
            {
                "patient_id": "P001", "timestamp": "2026-01-01 08:00:00",
                "age": 60, "sex": "F", "heart_rate": 80.0, "systolic_bp": 120.0,
                "diastolic_bp": 80.0, "spo2": 98.0, "respiratory_rate": 16.0,
                "temperature": 37.0, "lab_value_1": 1.0, "lab_value_2": 1.0,
                "diagnosis_category": "Sepsis", "medication_category": "None"
            },
            {
                "patient_id": "P001", "timestamp": "2026-01-01 09:00:00",
                "age": 60, "sex": "F", "heart_rate": 140.0, "systolic_bp": 80.0,
                "diastolic_bp": 45.0, "spo2": 85.0, "respiratory_rate": 35.0,
                "temperature": 40.0, "lab_value_1": 8.0, "lab_value_2": 4.0,
                "diagnosis_category": "Sepsis", "medication_category": "Oxygen"
            }
        ]
    }
    
    res = client.post("/predict", json=payload)
    assert res.status_code == 200
    pred = res.json()
    assert pred["patient_id"] == "P001"
    
    # 2. Priority check
    res = client.get("/api/patients/P001/priority")
    assert res.status_code == 200
    data = res.json()
    assert data["priority"] in ["Moderate", "High", "Critical"]
    
    # 3. Alert check
    res = client.get("/api/patients/P001/alerts")
    assert res.status_code == 200
    alerts = res.json()
    assert len(alerts) > 0
    assert "Patient priority changed" in alerts[-1]["message"]
    
    # 4. Timeline check
    res = client.get("/api/patients/P001/timeline")
    assert res.status_code == 200
    timeline = res.json()
    types = [t["type"] for t in timeline]
    assert "Priority Change" in types
    assert "Alert" in types
    
    # 5. Transfer
    res = client.post("/api/patients/P001/transfer", json={"receivingFacility": "ICU"})
    assert res.status_code == 200
    
    # 6. Generate Handover
    res = client.post("/api/patients/P001/handover", json={"receivingFacility": "ICU"})
    assert res.status_code == 200
    handover = res.json()
    handover_id = handover["id"]
    assert handover["status"] == "DRAFT"
    
    # 7. Clinician Review
    res = client.post(f"/api/handover/{handover_id}/review", json={"status": "APPROVED", "comments": "Looks good"})
    assert res.status_code == 200
    
    # 8. Final Report
    res = client.get(f"/api/handover/{handover_id}")
    assert res.status_code == 200
    report = res.json()
    assert "CLINICIAN-APPROVED FINAL REPORT" in report["status_label"]
    assert "Looks good" in report["report_content"]


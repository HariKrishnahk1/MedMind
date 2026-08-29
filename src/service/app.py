"""
FastAPI Prediction Service for Clinical Deterioration Prediction Engine.

Exposes REST endpoint `POST /predict` to evaluate longitudinal clinical observations
and return deterioration risk probability, risk category, and SHAP explainability feature contributions.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.models.predict import DeteriorationPredictor
from src.service.db import mock_patients, mock_alerts, mock_predictions, mock_timelines
from src.service.member4 import (
    update_patient_priority,
    execute_patient_transfer,
    generate_ai_handover,
    review_handover,
    get_final_report
)

DISCLAIMER_TEXT = (
    "Research prototype only. Predictions are generated from synthetic/de-identified data "
    "and have not been clinically validated. Predictions must not be used independently for "
    "diagnosis or treatment. Clinical interpretation and treatment decisions remain the "
    "responsibility of qualified healthcare professionals."
)

predictor_instance: Optional[DeteriorationPredictor] = None

@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    global predictor_instance
    try:
        predictor_instance = DeteriorationPredictor()
        print("DeteriorationPredictor successfully loaded into API service.")
    except Exception as e:
        print(f"Error loading DeteriorationPredictor: {e}")
    yield

app = FastAPI(
    title="AI Clinical Deterioration Prediction Engine Service",
    description=f"Continuous clinical observation monitoring and deterioration prediction API.\n\n**Safety Disclaimer**: {DISCLAIMER_TEXT}",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_predictor() -> DeteriorationPredictor:
    global predictor_instance
    if predictor_instance is None:
        predictor_instance = DeteriorationPredictor()
    return predictor_instance

class ObservationItem(BaseModel):
    patient_id: str = Field(..., json_schema_extra={"example": "P0001"}, description="Unique patient identifier")
    timestamp: str = Field(..., json_schema_extra={"example": "2026-01-01 12:00:00"}, description="Observation timestamp")
    age: int = Field(..., ge=0, le=120, json_schema_extra={"example": 65})
    sex: str = Field(..., json_schema_extra={"example": "M"})
    heart_rate: float = Field(..., json_schema_extra={"example": 82.0})
    systolic_bp: float = Field(..., json_schema_extra={"example": 118.0})
    diastolic_bp: float = Field(..., json_schema_extra={"example": 76.0})
    spo2: Optional[float] = Field(None, json_schema_extra={"example": 97.5})
    respiratory_rate: Optional[float] = Field(None, json_schema_extra={"example": 18.0})
    temperature: Optional[float] = Field(None, json_schema_extra={"example": 36.9})
    lab_value_1: Optional[float] = Field(None, json_schema_extra={"example": 1.4})
    lab_value_2: Optional[float] = Field(None, json_schema_extra={"example": 0.9})
    diagnosis_category: Optional[str] = Field("General", json_schema_extra={"example": "Sepsis"})
    medication_category: Optional[str] = Field("None", json_schema_extra={"example": "Oxygen"})

class PredictionRequest(BaseModel):
    observations: List[ObservationItem] = Field(..., min_length=1, description="Chronological patient observations")
    prediction_horizon_minutes: Optional[int] = Field(None, ge=5, le=1440, json_schema_extra={"example": 15})

class FeatureExplanationItem(BaseModel):
    feature: str
    contribution: float
    direction: str
    feature_value: Optional[Any] = None

class PredictionResponse(BaseModel):
    patient_id: str
    risk_score: float
    risk_level: str
    prediction_horizon_minutes: int
    model_version: str
    explanation: List[FeatureExplanationItem]
    disclaimer: str = DISCLAIMER_TEXT

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Health check status endpoint."""
    predictor = get_predictor()
    return {
        "status": "healthy",
        "service": "AI Deterioration Engine API",
        "model_version": predictor.model_version
    }

@app.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict near-term patient clinical deterioration risk"
)
def predict_deterioration(request: PredictionRequest):
    """
    Receives longitudinal patient observations, extracts trajectory features,
    and returns near-term deterioration probability + SHAP explanation.
    """
    predictor = get_predictor()
    if not request.observations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one clinical observation must be provided."
        )
        
    obs_dicts = [obs.model_dump() for obs in request.observations]
    
    try:
        prediction_result = predictor.predict(
            observations=obs_dicts,
            horizon_minutes=request.prediction_horizon_minutes
        )
        prediction_result["disclaimer"] = DISCLAIMER_TEXT
        
        # Member 4: Dynamic Priority Update based on prediction risk
        update_patient_priority(obs_dicts[0]["patient_id"], prediction_result)
        
        return prediction_result
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction computation failed: {str(e)}"
        )

@app.get("/api/patients")
def get_patients():
    return mock_patients

@app.get("/api/patients/{patient_id}")
def get_patient(patient_id: str):
    patient = next((p for p in mock_patients if p["id"] == patient_id), None)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.get("/api/patients/{patient_id}/predictions")
def get_predictions(patient_id: str):
    return mock_predictions.get(patient_id, [])

@app.get("/api/patients/{patient_id}/timeline")
def get_timeline(patient_id: str):
    return mock_timelines.get(patient_id, [])

@app.get("/api/alerts")
def get_alerts():
    return mock_alerts

@app.post("/api/alerts/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: str):
    alert = next((a for a in mock_alerts if a["id"] == alert_id), None)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert["status"] = "Acknowledged"
    return {"success": True}

@app.get("/api/patients/{patient_id}/priority")
def get_patient_priority(patient_id: str):
    patient = next((p for p in mock_patients if p["id"] == patient_id), None)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"patient_id": patient_id, "priority": patient.get("priority", "Stable")}

@app.get("/api/patients/{patient_id}/alerts")
def get_patient_alerts(patient_id: str):
    return [a for a in mock_alerts if a["patientId"] == patient_id]

class HandoverRequest(BaseModel):
    receivingFacility: str

@app.post("/api/patients/{patient_id}/transfer")
def transfer_patient(patient_id: str, req: HandoverRequest):
    try:
        return execute_patient_transfer(patient_id, req.receivingFacility)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/patients/{patient_id}/handover")
def generate_ai_handover_endpoint(patient_id: str, req: HandoverRequest):
    try:
        return generate_ai_handover(patient_id, req.receivingFacility)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

class ReviewRequest(BaseModel):
    status: str
    comments: str = ""

@app.post("/api/handover/{handover_id}/review")
def review_handover_endpoint(handover_id: str, req: ReviewRequest):
    try:
        return review_handover(handover_id, req.status, req.comments)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/handover/{handover_id}")
def get_final_report_endpoint(handover_id: str):
    try:
        return get_final_report(handover_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


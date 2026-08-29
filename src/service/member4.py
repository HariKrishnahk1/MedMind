import datetime
import uuid
import os
import json
import urllib.request
from typing import Dict, Any, List

from src.service.db import mock_patients, mock_alerts, mock_predictions, mock_timelines

mock_handovers: Dict[str, Dict[str, Any]] = {}

def get_current_time_str() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def update_patient_priority(patient_id: str, prediction_result: dict):
    patient = next((p for p in mock_patients if p["id"] == patient_id), None)
    if not patient:
        return
    
    current_priority = patient.get("priority", "Stable")
    risk_score = prediction_result.get("risk_score", 0.0)
    risk_level = prediction_result.get("risk_level", "low")
    
    if risk_level == "low":
        new_priority = "Stable"
    elif risk_level == "medium":
        new_priority = "Moderate"
    elif risk_level == "high":
        if risk_score >= 0.75:
            new_priority = "Critical"
        else:
            new_priority = "High"
    else:
        new_priority = current_priority

    if current_priority != new_priority:
        patient["priority"] = new_priority
        timestamp = get_current_time_str()
        
        timeline_event = {
            "id": f"TL-{uuid.uuid4().hex[:8]}",
            "patientId": patient_id,
            "timestamp": timestamp,
            "type": "Priority Change",
            "title": f"Priority changed to {new_priority}",
            "description": f"Priority updated from {current_priority} to {new_priority} based on AI Risk Assessment.",
            "priorityAtTime": new_priority
        }
        if patient_id not in mock_timelines:
            mock_timelines[patient_id] = []
        mock_timelines[patient_id].append(timeline_event)
        
        alert = {
            "id": f"ALT-{uuid.uuid4().hex[:8]}",
            "patientId": patient_id,
            "timestamp": timestamp,
            "type": "Priority Alert",
            "message": f"Patient priority changed to {new_priority}",
            "previousPriority": current_priority,
            "newPriority": new_priority,
            "risk_score": risk_score,
            "status": "Unacknowledged",
            "reason": "AI Risk Assessment triggered priority change",
            "clinicalFactors": [exp.get("feature") for exp in prediction_result.get("explanation", [])][:3]
        }
        mock_alerts.append(alert)
        
        alert_event = {
            "id": f"TL-{uuid.uuid4().hex[:8]}",
            "patientId": patient_id,
            "timestamp": timestamp,
            "type": "Alert",
            "title": f"{new_priority} Deterioration Alert",
            "description": f"System generated alert due to priority change to {new_priority}.",
            "priorityAtTime": new_priority
        }
        mock_timelines[patient_id].append(alert_event)

def execute_patient_transfer(patient_id: str, receiving_facility: str) -> dict:
    patient = next((p for p in mock_patients if p["id"] == patient_id), None)
    if not patient:
        raise ValueError("Patient not found")
        
    timestamp = get_current_time_str()
    
    transfer_event = {
        "id": f"TL-{uuid.uuid4().hex[:8]}",
        "patientId": patient_id,
        "timestamp": timestamp,
        "type": "Transfer",
        "title": f"Transfer to {receiving_facility}",
        "description": f"Patient transfer initiated to {receiving_facility}.",
        "priorityAtTime": patient.get("priority", "Unknown")
    }
    
    if patient_id not in mock_timelines:
        mock_timelines[patient_id] = []
    mock_timelines[patient_id].append(transfer_event)
    
    return {"status": "Transfer Initiated", "receiving_facility": receiving_facility, "timestamp": timestamp}

def generate_ai_handover(patient_id: str, receiving_facility: str) -> dict:
    patient = next((p for p in mock_patients if p["id"] == patient_id), None)
    if not patient:
        raise ValueError("Patient not found")
    
    timeline = mock_timelines.get(patient_id, [])
    alerts = [a for a in mock_alerts if a["patientId"] == patient_id]
    predictions = mock_predictions.get(patient_id, [])
    
    latest_prediction = predictions[-1] if predictions else None
    
    prompt = f"""You are a clinical AI assistant generating an explainable clinical handover report.
Synthesize ONLY the provided information. Do not invent any values, diagnoses, or treatments.
If information is missing, write "Not available in the provided clinical record."

Patient Info:
Name: {patient.get("name")}, Age: {patient.get("age")}, Gender: {patient.get("gender")}, MRN: {patient.get("mrn")}
Diagnosis: {patient.get("primaryDiagnosis")}
Allergies: {', '.join(patient.get("allergies", []))}
Priority: {patient.get("priority")}
Receiving Facility: {receiving_facility}

Vitals: {json.dumps(patient.get("vitals"))}
Latest AI Risk: {json.dumps(latest_prediction) if latest_prediction else 'None'}
Recent Alerts: {json.dumps(alerts[-3:]) if alerts else 'None'}"""
    
    ai_api_key = os.getenv("AI_API_KEY")
    draft_content = ""
    
    if ai_api_key:
        try:
            req = urllib.request.Request(
                "https://api.openai.com/v1/chat/completions",
                data=json.dumps({
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "system", "content": prompt}]
                }).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {ai_api_key}"
                }
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode())
                draft_content = result["choices"][0]["message"]["content"]
        except Exception as e:
            draft_content = "AI API unavailable. " + str(e)
    else:
        draft_content = (
            f"**AI-GENERATED DRAFT**\n\n"
            f"PATIENT OVERVIEW\n"
            f"{patient.get('name')}, {patient.get('age')}yo {patient.get('gender')}. MRN: {patient.get('mrn')}.\n"
            f"Diagnosis: {patient.get('primaryDiagnosis', 'Not available in the provided clinical record.')}\n"
            f"Allergies: {', '.join(patient.get('allergies', []))}\n\n"
            f"CURRENT INFORMATION & VITALS\n"
            f"{json.dumps(patient.get('vitals', {}))}\n\n"
            f"AI RISK ASSESSMENT & EXPLAINABLE AI FACTORS\n"
            f"{json.dumps(latest_prediction) if latest_prediction else 'Not available in the provided clinical record.'}\n\n"
            f"PRIORITY HISTORY & ALERTS\n"
            f"Current Priority: {patient.get('priority')}\n"
            f"Alerts: {len(alerts)}\n\n"
            f"HANDOVER SUMMARY\n"
            f"Transferring to {receiving_facility}."
        )

    handover_id = f"HO-{uuid.uuid4().hex[:8]}"
    timestamp = get_current_time_str()
    
    handover = {
        "id": handover_id,
        "patientId": patient_id,
        "receivingFacility": receiving_facility,
        "timestamp": timestamp,
        "status": "DRAFT",
        "content": draft_content,
        "clinician_review": None
    }
    
    mock_handovers[handover_id] = handover
    
    timeline_event = {
        "id": f"TL-{uuid.uuid4().hex[:8]}",
        "patientId": patient_id,
        "timestamp": timestamp,
        "type": "Handover Generated",
        "title": "AI Handover Draft Generated",
        "description": "An AI-assisted handover draft was created and is pending review.",
        "priorityAtTime": patient.get("priority", "Unknown")
    }
    if patient_id not in mock_timelines:
        mock_timelines[patient_id] = []
    mock_timelines[patient_id].append(timeline_event)
    
    return handover

def review_handover(handover_id: str, status: str, comments: str = "") -> dict:
    handover = mock_handovers.get(handover_id)
    if not handover:
        raise ValueError("Handover not found")
        
    if status not in ["APPROVED", "NEEDS_REVISION"]:
        raise ValueError("Invalid review state")
        
    handover["status"] = status
    handover["clinician_review"] = {
        "status": status,
        "comments": comments,
        "timestamp": get_current_time_str()
    }
    
    timeline_event = {
        "id": f"TL-{uuid.uuid4().hex[:8]}",
        "patientId": handover["patientId"],
        "timestamp": get_current_time_str(),
        "type": "Clinician Review",
        "title": f"Handover Review: {status}",
        "description": f"Clinician reviewed handover draft. Status: {status}.",
        "priorityAtTime": next((p.get("priority", "Unknown") for p in mock_patients if p["id"] == handover["patientId"]), "Unknown")
    }
    mock_timelines[handover["patientId"]].append(timeline_event)
    
    return handover

def get_final_report(handover_id: str) -> dict:
    handover = mock_handovers.get(handover_id)
    if not handover:
        raise ValueError("Handover not found")
        
    patient = next((p for p in mock_patients if p["id"] == handover["patientId"]), None)
    
    status_label = "CLINICIAN-APPROVED FINAL REPORT" if handover["status"] == "APPROVED" else "AI-GENERATED DRAFT"
    
    report_content = f"=========================================\n" \
                     f"{status_label}\n" \
                     f"=========================================\n" \
                     f"Timestamp: {handover['timestamp']}\n" \
                     f"Model Version: model_v1\n" \
                     f"=========================================\n\n" \
                     f"{handover['content']}\n\n" \
                     f"=========================================\n" \
                     f"CLINICIAN REVIEW STATUS: {handover['status']}\n" \
                     f"COMMENTS: {handover.get('clinician_review', {}).get('comments', 'None')}\n" \
                     f"=========================================\n"
    
    return {
        "handover_id": handover_id,
        "patient_id": handover["patientId"],
        "status_label": status_label,
        "report_content": report_content
    }

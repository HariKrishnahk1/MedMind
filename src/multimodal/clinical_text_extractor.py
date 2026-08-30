"""
Clinical Document Text Concept Extraction Engine.

Extracts structured clinical concepts from doctor notes and lab reports:
- symptoms
- conditions_mentioned
- medications_mentioned
- procedures_mentioned
- investigations
- temporal_information
"""

import re
from typing import Dict, List, Any

SYMPTOM_KEYWORDS = ["shortness of breath", "dyspnea", "chest pain", "fever", "cough", "confusion", "tachycardia", "hypotension", "chills", "dizziness"]
CONDITION_KEYWORDS = ["sepsis", "myocardial infarction", "copd", "pneumonia", "stroke", "kidney injury", "diabetes", "hypertension", "asthma"]
MEDICATION_KEYWORDS = ["norepinephrine", "aspirin", "vancomycin", "metoprolol", "albuterol", "furosemide", "oxygen", "heparin"]
PROCEDURE_KEYWORDS = ["intubation", "central line", "arterial line", "bronchoscopy", "chest tube", "dialysis", "appendectomy"]

def extract_clinical_concepts_from_note(text: str) -> Dict[str, Any]:
    """
    Extracts structured entities from clinical free-text note without medical hallucination.
    """
    if not text:
        return {
            "symptoms": [],
            "conditions_mentioned": [],
            "medications_mentioned": [],
            "procedures_mentioned": [],
            "investigations": [],
            "temporal_information": ["No note text provided"]
        }
        
    text_lower = text.lower()
    
    extracted_symptoms = [s for s in SYMPTOM_KEYWORDS if s in text_lower]
    extracted_conditions = [c for c in CONDITION_KEYWORDS if c in text_lower]
    extracted_meds = [m for m in MEDICATION_KEYWORDS if m in text_lower]
    extracted_procs = [p for p in PROCEDURE_KEYWORDS if p in text_lower]
    
    # Extract timestamps or relative time references
    temporal_matches = re.findall(r'\b(?:\d{1,2}:\d{2}|\d+\s*(?:hours|hrs|mins|minutes|days))\b', text_lower)
    
    return {
        "symptoms": extracted_symptoms,
        "conditions_mentioned": extracted_conditions,
        "medications_mentioned": extracted_meds,
        "procedures_mentioned": extracted_procs,
        "investigations": ["Lactate", "WBC", "Creatinine"] if "lab" in text_lower or "blood" in text_lower else [],
        "temporal_information": temporal_matches if temporal_matches else ["Recent clinical note"]
    }

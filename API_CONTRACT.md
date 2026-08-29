# API Contract — Clinical Deterioration Prediction Engine

**Version**: 1.0.0  
**Protocol**: REST / HTTP  
**Service Endpoint Base**: `http://localhost:8000`  

> [!IMPORTANT]
> **Safety Disclaimer**: Research prototype only. Predictions are generated from synthetic/de-identified data and have not been clinically validated. Predictions must not be used independently for diagnosis or treatment. Clinical interpretation and treatment decisions remain the responsibility of qualified healthcare professionals.

---

## 1. Health Check Endpoint

### `GET /health`

Checks service health and reports active model version.

#### Response Schema (`200 OK`)
```json
{
  "status": "healthy",
  "service": "AI Deterioration Engine API",
  "model_version": "random_forest"
}
```

---

## 2. Deterioration Prediction Endpoint

### `POST /predict`

Predicts near-term clinical deterioration probability and generates SHAP feature contributions for a given patient based on longitudinal observations.

---

### Request Specification

#### Headers
`Content-Type: application/json`

#### Request Body Schema (`PredictionRequest`)
| Field | Type | Required | Description |
|---|---|---|---|
| `observations` | `Array<ObservationItem>` | **Yes** | Chronological list of clinical observations for a single patient (min 1). |
| `prediction_horizon_minutes` | `Integer` | No | Overrides default prediction lookahead window in minutes (default: `15`). |

#### Observation Item Schema (`ObservationItem`)
| Field | Type | Required | Range / Example | Description |
|---|---|---|---|---|
| `patient_id` | `String` | **Yes** | `"P0001"` | Unique patient identifier |
| `timestamp` | `String` | **Yes** | `"2026-01-01 12:00:00"` | ISO format observation timestamp |
| `age` | `Integer` | **Yes** | `18 - 120` | Patient age in years |
| `sex` | `String` | **Yes** | `"M"` / `"F"` | Biological sex |
| `heart_rate` | `Float` | **Yes** | `20 - 250` | Heart rate (bpm) |
| `systolic_bp` | `Float` | **Yes** | `40 - 300` | Systolic blood pressure (mmHg) |
| `diastolic_bp` | `Float` | **Yes** | `20 - 200` | Diastolic blood pressure (mmHg) |
| `spo2` | `Float` | No | `50.0 - 100.0` | Oxygen saturation (%) |
| `respiratory_rate` | `Float` | No | `4.0 - 60.0` | Respiratory rate (breaths/min) |
| `temperature` | `Float` | No | `30.0 - 45.0` | Body temperature (°C) |
| `lab_value_1` | `Float` | No | `0.0 - 30.0` | Serum Lactate (mmol/L) |
| `lab_value_2` | `Float` | No | `0.0 - 20.0` | Serum Creatinine (mg/dL) |
| `diagnosis_category` | `String` | No | `"Sepsis"` | Primary admission category |
| `medication_category` | `String` | No | `"Oxygen"` | Current active medication class |

---

### Request Payload Example

```json
{
  "prediction_horizon_minutes": 15,
  "observations": [
    {
      "patient_id": "P0001",
      "timestamp": "2026-01-01 08:00:00",
      "age": 65,
      "sex": "M",
      "heart_rate": 78.0,
      "systolic_bp": 120.0,
      "diastolic_bp": 75.0,
      "spo2": 98.0,
      "respiratory_rate": 16.0,
      "temperature": 36.8,
      "lab_value_1": 1.2,
      "lab_value_2": 0.9,
      "diagnosis_category": "Sepsis",
      "medication_category": "None"
    },
    {
      "patient_id": "P0001",
      "timestamp": "2026-01-01 09:00:00",
      "age": 65,
      "sex": "M",
      "heart_rate": 115.0,
      "systolic_bp": 92.0,
      "diastolic_bp": 58.0,
      "spo2": 91.0,
      "respiratory_rate": 26.0,
      "temperature": 38.5,
      "lab_value_1": 3.8,
      "lab_value_2": 1.6,
      "diagnosis_category": "Sepsis",
      "medication_category": "Oxygen"
    }
  ]
}
```

---

### Response Specification

#### Success Response Schema (`200 OK`)
| Field | Type | Description |
|---|---|---|
| `patient_id` | `String` | Patient ID associated with prediction |
| `risk_score` | `Float` | Probability of deterioration (`0.0` to `1.0`) |
| `risk_level` | `String` | Categorized risk: `"low"`, `"medium"`, or `"high"` |
| `prediction_horizon_minutes` | `Integer` | Evaluation horizon window in minutes |
| `model_version` | `String` | Identifier of active ML model artifact |
| `explanation` | `Array<FeatureExplanationItem>` | Top N features driving model prediction ranked by SHAP value |
| `disclaimer` | `String` | Mandatory research prototype safety disclaimer |

#### Feature Explanation Item (`FeatureExplanationItem`)
| Field | Type | Description |
|---|---|---|
| `feature` | `String` | Name of clinical feature |
| `contribution` | `Float` | SHAP contribution score (+ raises risk, - lowers risk) |
| `direction` | `String` | `"increased_risk"`, `"decreased_risk"`, or `"neutral"` |
| `feature_value` | `Any` | Original unscaled observation value |

#### Response Payload Example

```json
{
  "patient_id": "P0001",
  "risk_score": 0.8742,
  "risk_level": "high",
  "prediction_horizon_minutes": 15,
  "model_version": "random_forest",
  "explanation": [
    {
      "feature": "lab_value_1_change_from_baseline",
      "contribution": 0.3842,
      "direction": "increased_risk",
      "feature_value": 2.6
    },
    {
      "feature": "spo2_change_from_baseline",
      "contribution": 0.2415,
      "direction": "increased_risk",
      "feature_value": -7.0
    },
    {
      "feature": "heart_rate_recent_mean",
      "contribution": 0.1820,
      "direction": "increased_risk",
      "feature_value": 96.5
    },
    {
      "feature": "respiratory_rate_trend_slope",
      "contribution": 0.1105,
      "direction": "increased_risk",
      "feature_value": 5.0
    },
    {
      "feature": "systolic_bp_current",
      "contribution": 0.0890,
      "direction": "increased_risk",
      "feature_value": 92.0
    }
  ],
  "disclaimer": "Research prototype only. Predictions are generated from synthetic/de-identified data and have not been clinically validated. Predictions must not be used independently for diagnosis or treatment. Clinical interpretation and treatment decisions remain the responsibility of qualified healthcare professionals."
}
```

---

## 3. Error Responses

| HTTP Code | Error Title | Description / Resolution |
|---|---|---|
| `400 Bad Request` | Validation Error | Missing required fields, invalid datatypes, invalid clinical bounds, or empty observations array. |
| `422 Unprocessable Entity` | Schema Error | Request body fails Pydantic schema validation. |
| `500 Internal Server Error` | Model Failure | Error during preprocessing or SHAP calculation. |
| `503 Service Unavailable` | Service Uninitialized | Model artifacts not yet loaded into API memory. |

#### Error Payload Example (`400 Bad Request`)
```json
{
  "detail": "Input validation error: ['Missing required columns: [heart_rate]']"
}
```

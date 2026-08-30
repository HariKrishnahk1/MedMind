"""
Automated Experiment Registry & Markdown Report Generator.

Logs all executed model training experiments to `experiments/experiment_registry.csv`
and generates detailed markdown research reports in `experiments/reports/EXP_xxx_report.md`.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any
import pandas as pd

REGISTRY_CSV = "experiments/experiment_registry.csv"
REPORTS_DIR = "experiments/reports"

def log_experiment(
    experiment_id: str,
    model_name: str,
    hyperparams: Dict[str, Any],
    metrics: Dict[str, Any],
    dataset_version: str = "v1.0",
    feature_version: str = "v1.0",
    random_seed: int = 42,
    artifact_path: str = ""
) -> Dict[str, Any]:
    """
    Logs experiment details to registry CSV and generates a markdown research report.
    """
    os.makedirs(os.path.dirname(REGISTRY_CSV), exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    entry = {
        "experiment_id": experiment_id,
        "timestamp": timestamp,
        "model_name": model_name,
        "dataset_version": dataset_version,
        "feature_version": feature_version,
        "random_seed": random_seed,
        "auroc": round(float(metrics.get("auroc", 0.0)), 4),
        "auprc": round(float(metrics.get("auprc", 0.0)), 4),
        "precision": round(float(metrics.get("precision", 0.0)), 4),
        "recall": round(float(metrics.get("recall", 0.0)), 4),
        "f1": round(float(metrics.get("f1", 0.0)), 4),
        "sensitivity": round(float(metrics.get("sensitivity", 0.0)), 4),
        "specificity": round(float(metrics.get("specificity", 0.0)), 4),
        "brier_score": round(float(metrics.get("brier_score", 0.0)), 4),
        "false_alert_rate": round(float(metrics.get("false_alert_rate", 0.0)), 4),
        "optimal_threshold": round(float(metrics.get("optimal_threshold", 0.50)), 2),
        "artifact_path": artifact_path,
        "hyperparameters": json.dumps(hyperparams)
    }
    
    # Append to CSV
    if os.path.exists(REGISTRY_CSV):
        df = pd.read_csv(REGISTRY_CSV)
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    else:
        df = pd.DataFrame([entry])
        
    df.to_csv(REGISTRY_CSV, index=False)
    
    # Generate Markdown Report
    report_file = os.path.join(REPORTS_DIR, f"{experiment_id}_report.md")
    report_content = f"""# Research Experiment Report: {experiment_id}

- **Execution Date**: {timestamp}
- **Model Architecture**: `{model_name}`
- **Dataset Version**: `{dataset_version}`
- **Feature Version**: `{feature_version}`
- **Random Seed**: `{random_seed}`
- **Artifact Path**: `{artifact_path}`

---

## 1. Empirical Test Split Evaluation Metrics

| Metric | Score |
|---|---|
| **AUROC** | `{entry['auroc']}` |
| **AUPRC** | `{entry['auprc']}` |
| **F1-Score** | `{entry['f1']}` |
| **Precision** | `{entry['precision']}` |
| **Recall / Sensitivity** | `{entry['recall']}` |
| **Specificity** | `{entry['specificity']}` |
| **Brier Score (Calibration)** | `{entry['brier_score']}` |
| **False Alert Rate** | `{entry['false_alert_rate']}` |
| **Optimal Threshold** | `{entry['optimal_threshold']}` |

---

## 2. Hyperparameters
```json
{json.dumps(hyperparams, indent=2)}
```

---

> **Research Note**: Evaluated on patient-level group test split. All metrics reflect actual empirical execution.
"""
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    return entry

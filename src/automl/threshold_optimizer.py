"""
Precision-Recall Decision Threshold Optimization Engine.

Evaluates sensitivity, specificity, precision, F1-score, and false-alert rate across
decision thresholds from 0.10 to 0.90. Exports empirical threshold trade-off metrics
to `experiments/threshold_analysis.csv`.
"""

import os
from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

def optimize_decision_threshold(
    y_test: np.ndarray,
    y_probs: np.ndarray,
    output_csv: str = "experiments/threshold_analysis.csv"
) -> Dict[str, Any]:
    """
    Evaluates classification performance across decision thresholds.
    """
    thresholds = np.linspace(0.10, 0.90, 17)
    records = []
    
    best_threshold = 0.50
    best_f1 = -1.0
    
    for th in thresholds:
        preds = (y_probs >= th).astype(int)
        cm = confusion_matrix(y_test, preds)
        tn, fp, fn, tp = cm.ravel() if cm.shape == (2, 2) else (0, 0, 0, 0)
        
        sens = recall_score(y_test, preds, zero_division=0)
        spec = tn / max(tn + fp, 1)
        prec = precision_score(y_test, preds, zero_division=0)
        f1 = f1_score(y_test, preds, zero_division=0)
        far = fp / max(fp + tn, 1)
        
        record = {
            "threshold": round(float(th), 2),
            "sensitivity": round(float(sens), 4),
            "specificity": round(float(spec), 4),
            "precision": round(float(prec), 4),
            "f1_score": round(float(f1), 4),
            "false_alert_rate": round(float(far), 4),
            "tp": int(tp),
            "fp": int(fp),
            "tn": int(tn),
            "fn": int(fn)
        }
        records.append(record)
        
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = round(float(th), 2)
            
    df_res = pd.DataFrame(records)
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_res.to_csv(output_csv, index=False)
    
    return {
        "best_threshold": best_threshold,
        "best_f1_score": round(float(best_f1), 4),
        "threshold_analysis_path": output_csv,
        "metrics_summary": records
    }

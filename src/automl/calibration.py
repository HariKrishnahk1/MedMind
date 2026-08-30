"""
Probability Calibration & Reliability Analysis Engine.

Performs Platt Scaling (Sigmoid) and Isotonic Regression probability calibration.
Evaluates raw vs calibrated Brier Score Loss and reliability curve metrics.
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import brier_score_loss

def calibrate_model_probabilities(
    model: Any,
    X_train: pd.DataFrame,
    y_train: np.ndarray,
    X_test: pd.DataFrame,
    y_test: np.ndarray,
    method: str = "sigmoid"
) -> Tuple[Any, Dict[str, Any]]:
    """
    Fits probability calibrator on training data and computes test Brier scores and calibration curves.
    """
    # Raw probabilities
    raw_probs = model.predict_proba(X_test)[:, 1]
    raw_brier = brier_score_loss(y_test, raw_probs)
    
    # Calibrated Classifier
    calibrated_model = CalibratedClassifierCV(estimator=model, method=method, cv=3)
    calibrated_model.fit(X_train, y_train)
    
    cal_probs = calibrated_model.predict_proba(X_test)[:, 1]
    cal_brier = brier_score_loss(y_test, cal_probs)
    
    # Reliability curve points
    prob_true_raw, prob_pred_raw = calibration_curve(y_test, raw_probs, n_bins=10)
    prob_true_cal, prob_pred_cal = calibration_curve(y_test, cal_probs, n_bins=10)
    
    metrics = {
        "calibration_method": method,
        "raw_brier_score": round(float(raw_brier), 4),
        "calibrated_brier_score": round(float(cal_brier), 4),
        "brier_score_improvement": round(float(raw_brier - cal_brier), 4),
        "reliability_curve": {
            "raw": {"prob_true": prob_true_raw.tolist(), "prob_pred": prob_pred_raw.tolist()},
            "calibrated": {"prob_true": prob_true_cal.tolist(), "prob_pred": prob_pred_cal.tolist()}
        }
    }
    
    return calibrated_model, metrics

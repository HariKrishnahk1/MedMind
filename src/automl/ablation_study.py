"""
Automated Feature Ablation Framework.

Compares model performance across four distinct feature configurations:
- Exp A: Raw clinical observations
- Exp B: Raw + temporal features
- Exp C: Raw + temporal + patient baseline features
- Exp D: Raw + temporal + baseline + missingness pattern features

Outputs empirical results to `experiments/ablation_results.csv`.
"""

import os
from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score, brier_score_loss

def run_ablation_study(
    processed_dataset_path: str = "data/processed/model_dataset.csv",
    output_csv: str = "experiments/ablation_results.csv",
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Executes automated feature ablation study comparing raw vs temporal vs baseline vs full feature sets.
    """
    if not os.path.exists(processed_dataset_path):
        raise FileNotFoundError(f"Dataset not found at {processed_dataset_path}")
        
    df = pd.read_csv(processed_dataset_path)
    df = df.loc[:, ~df.columns.duplicated()]
    
    # Feature group definitions
    raw_vitals = ["heart_rate", "systolic_bp", "diastolic_bp", "spo2", "respiratory_rate", "temperature"]
    temporal_feats = [c for c in df.columns if "rolling" in c or "slope" in c or "change" in c or "time_since" in c]
    baseline_feats = [c for c in df.columns if "baseline" in c or "dev" in c]
    missing_feats = [c for c in df.columns if "missing" in c or "isnan" in c]
    
    all_features = [c for c in df.columns if c not in ["patient_id", "timestamp", "target_deterioration", "sex", "diagnosis_category", "medication_category"]]
    
    feature_sets = {
        "Exp A (Raw Clinical Vitals)": [f for f in raw_vitals if f in df.columns],
        "Exp B (Raw + Temporal)": [f for f in raw_vitals + temporal_feats if f in df.columns],
        "Exp C (Raw + Temporal + Baseline)": [f for f in raw_vitals + temporal_feats + baseline_feats if f in df.columns],
        "Exp D (Full Architecture: Raw + Temp + Base + Missingness)": [f for f in all_features if f in df.columns]
    }
    
    # Patient-level split
    patients = df["patient_id"].unique()
    np.random.seed(random_seed)
    train_patients = np.random.choice(patients, size=int(len(patients) * 0.8), replace=False)
    
    train_df = df[df["patient_id"].isin(train_patients)]
    test_df = df[~df["patient_id"].isin(train_patients)]
    
    y_train = train_df["target_deterioration"].values
    y_test = test_df["target_deterioration"].values
    
    results = []
    
    for set_name, raw_cols in feature_sets.items():
        cols = list(dict.fromkeys(raw_cols))
        if not cols:
            continue
            
        X_train = train_df[cols].fillna(0)
        X_test = test_df[cols].fillna(0)
        
        clf = RandomForestClassifier(n_estimators=50, max_depth=6, random_state=random_seed, class_weight="balanced")
        clf.fit(X_train, y_train)
        
        probs = clf.predict_proba(X_test)[:, 1]
        preds = (probs >= 0.5).astype(int)
        
        auroc = roc_auc_score(y_test, probs)
        f1 = f1_score(y_test, preds, zero_division=0)
        prec = precision_score(y_test, preds, zero_division=0)
        rec = recall_score(y_test, preds, zero_division=0)
        brier = brier_score_loss(y_test, probs)
        
        results.append({
            "experiment": set_name,
            "feature_count": len(cols),
            "auroc": round(float(auroc), 4),
            "f1_score": round(float(f1), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "brier_score": round(float(brier), 4)
        })
        
    res_df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    res_df.to_csv(output_csv, index=False)
    
    return res_df

"""
Missing-Data Robustness Experiment Framework.

Artificially introduces 5%, 10%, 20%, and 30% random missingness into evaluation features
to measure model performance degradation and missing-data robustness.
Outputs results to `experiments/missingness_results.csv`.
"""

import os
from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score, brier_score_loss

def run_robustness_experiment(
    processed_dataset_path: str = "data/processed/model_dataset.csv",
    output_csv: str = "experiments/missingness_results.csv",
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Evaluates model performance under artificial missingness levels (5%, 10%, 20%, 30%).
    """
    if not os.path.exists(processed_dataset_path):
        raise FileNotFoundError(f"Dataset not found at {processed_dataset_path}")
        
    df = pd.read_csv(processed_dataset_path)
    df = df.loc[:, ~df.columns.duplicated()]
    feature_cols = [c for c in df.columns if c not in ["patient_id", "timestamp", "target_deterioration", "sex", "diagnosis_category", "medication_category"]]
    
    patients = df["patient_id"].unique()
    np.random.seed(random_seed)
    train_patients = np.random.choice(patients, size=int(len(patients) * 0.8), replace=False)
    
    train_df = df[df["patient_id"].isin(train_patients)]
    test_df = df[~df["patient_id"].isin(train_patients)]
    
    X_train = train_df[feature_cols].fillna(0)
    y_train = train_df["target_deterioration"].values
    
    y_test = test_df["target_deterioration"].values
    
    # Fit base model
    clf = RandomForestClassifier(n_estimators=50, max_depth=6, random_state=random_seed, class_weight="balanced")
    clf.fit(X_train, y_train)
    
    missing_levels = [0.0, 0.05, 0.10, 0.20, 0.30]
    results = []
    
    for level in missing_levels:
        X_test_corrupted = test_df[feature_cols].copy()
        
        if level > 0.0:
            # Artificially inject NaN values
            mask = np.random.rand(*X_test_corrupted.shape) < level
            X_test_corrupted[mask] = np.nan
            
        X_test_imputed = X_test_corrupted.fillna(0)
        
        probs = clf.predict_proba(X_test_imputed)[:, 1]
        preds = (probs >= 0.5).astype(int)
        
        auroc = roc_auc_score(y_test, probs)
        f1 = f1_score(y_test, preds, zero_division=0)
        prec = precision_score(y_test, preds, zero_division=0)
        rec = recall_score(y_test, preds, zero_division=0)
        brier = brier_score_loss(y_test, probs)
        
        results.append({
            "missingness_level_pct": int(level * 100),
            "auroc": round(float(auroc), 4),
            "f1_score": round(float(f1), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "brier_score": round(float(brier), 4),
            "performance_retention_pct": round(float(auroc / (results[0]["auroc"] if results else auroc) * 100.0), 1)
        })
        
    res_df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    res_df.to_csv(output_csv, index=False)
    
    return res_df

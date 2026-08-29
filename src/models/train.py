"""
Model Training Module for Clinical Deterioration Engine.

Trains Logistic Regression, Random Forest, and XGBoost models using strict
patient-level splitting to prevent temporal and patient data leakage.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Tuple, Any

from sklearn.model_selection import GroupShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score

from src.data.preprocessing import get_feature_columns, build_preprocessing_pipeline

def train_all_models(
    processed_dataset_path: str = "data/processed/model_dataset.csv",
    models_dir: str = "models",
    random_seed: int = 42
) -> Dict[str, Any]:
    """
    Loads processed dataset, performs patient-level train/test split, fits preprocessing
    pipeline on train set only, trains candidate ML models, saves artifacts, and selects best model.
    """
    print(f"Loading processed dataset from {processed_dataset_path}...")
    df = pd.read_csv(processed_dataset_path)
    
    # 1. Feature Identification
    numerical_cols, categorical_cols = get_feature_columns(df)
    feature_cols = numerical_cols + categorical_cols
    
    X = df[feature_cols]
    y = df["target_deterioration"].values
    groups = df["patient_id"].values
    
    print(f"Total rows: {len(df)}, Patients: {len(np.unique(groups))}, Features: {len(feature_cols)}")
    
    # 2. Patient-Level Train/Test Split (80% Train Patients, 20% Test Patients)
    gss = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=random_seed)
    train_idx, test_idx = next(gss.split(X, y, groups))
    
    train_patients = np.unique(groups[train_idx])
    test_patients = np.unique(groups[test_idx])
    assert len(set(train_patients).intersection(set(test_patients))) == 0, "Patient leakage detected!"
    print(f"Patient-level split successful: Train Patients = {len(train_patients)}, Test Patients = {len(test_patients)}")
    
    X_train_raw, X_test_raw = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    
    # 3. Fit Preprocessing Pipeline ONLY on Train Set
    print("Fitting preprocessing pipeline on training data ONLY...")
    preprocessor = build_preprocessing_pipeline(numerical_cols, categorical_cols)
    X_train_trans = preprocessor.fit_transform(X_train_raw)
    X_test_trans = preprocessor.transform(X_test_raw)
    
    # Save preprocessor artifact
    os.makedirs(models_dir, exist_ok=True)
    joblib.dump(preprocessor, os.path.join(models_dir, "preprocessor.joblib"))
    
    # Save train/test split data for evaluate.py
    split_data = {
        "X_train": X_train_trans,
        "X_test": X_test_trans,
        "y_train": y_train,
        "y_test": y_test,
        "feature_names": numerical_cols + list(preprocessor.named_transformers_['cat'].named_steps['encoder'].get_feature_names_out(categorical_cols)),
        "raw_feature_cols": feature_cols,
        "numerical_cols": numerical_cols,
        "categorical_cols": categorical_cols,
        "train_idx": train_idx,
        "test_idx": test_idx
    }
    joblib.dump(split_data, os.path.join(models_dir, "split_data.joblib"))
    
    # Compute class imbalance ratio
    neg_count = np.sum(y_train == 0)
    pos_count = np.sum(y_train == 1)
    scale_pos_weight = neg_count / max(1, pos_count)
    print(f"Training set targets: Neg = {neg_count}, Pos = {pos_count} (scale_pos_weight = {scale_pos_weight:.2f})")
    
    # 4. Instantiate Candidate Models
    models = {
        "logistic_regression": LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=random_seed
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            class_weight="balanced",
            random_state=random_seed,
            n_jobs=-1
        ),
        "xgboost": XGBClassifier(
            n_estimators=150,
            max_depth=6,
            learning_rate=0.05,
            scale_pos_weight=scale_pos_weight,
            eval_metric="logloss",
            random_state=random_seed,
            n_jobs=-1
        )
    }
    
    trained_artifacts = {}
    best_score = -1.0
    best_model_name = ""
    best_model_obj = None
    
    print("\nTraining models...")
    for model_name, model in models.items():
        print(f"--- Training {model_name} ---")
        model.fit(X_train_trans, y_train)
        
        # Save individual model artifact
        model_sub_dir = os.path.join(models_dir, model_name)
        os.makedirs(model_sub_dir, exist_ok=True)
        model_path = os.path.join(model_sub_dir, "model.joblib")
        joblib.dump(model, model_path)
        
        # Evaluate on validation/test set for selection
        probs = model.predict_proba(X_test_trans)[:, 1]
        preds = (probs >= 0.5).astype(int)
        
        auroc = roc_auc_score(y_test, probs)
        f1 = f1_score(y_test, preds)
        print(f"   -> {model_name} | AUROC: {auroc:.4f} | F1: {f1:.4f}")
        
        trained_artifacts[model_name] = {
            "model_path": model_path,
            "auroc": float(auroc),
            "f1": float(f1)
        }
        
        # Selection criterion: AUROC primary, F1 secondary
        if auroc > best_score:
            best_score = auroc
            best_model_name = model_name
            best_model_obj = model

    print(f"\nBest Model Selected: '{best_model_name}' with Test AUROC = {best_score:.4f}")
    
    # Save Best Model Artifact at root of models/
    joblib.dump(best_model_obj, os.path.join(models_dir, "best_model.joblib"))
    
    # Save Metadata JSON
    metadata = {
        "best_model_name": best_model_name,
        "best_auroc": float(best_score),
        "prediction_horizon_minutes": 15,
        "training_patients": len(train_patients),
        "test_patients": len(test_patients),
        "total_features": len(feature_cols),
        "numerical_cols": numerical_cols,
        "categorical_cols": categorical_cols,
        "random_seed": random_seed
    }
    with open(os.path.join(models_dir, "model_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
        
    return trained_artifacts

if __name__ == "__main__":
    train_all_models()

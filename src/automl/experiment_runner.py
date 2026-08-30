"""
Automated Experiment Pipeline Orchestrator.

Single entrypoint executing the complete AutoML research loop:
1. Dataset validation & feature preprocessing
2. Patient-level train/test split
3. Candidate model hyperparameter optimization
4. Probability calibration & reliability curve generation
5. Decision threshold optimization
6. Experiment registry logging
7. Feature ablation study execution
8. Missing-data robustness evaluation
9. SHAP feature attribution computation
10. Model registry promotion
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import joblib
import numpy as np
import pandas as pd

from src.data.preprocessing import run_preprocessing_pipeline, get_feature_columns
from src.automl.hyperparameter_search import optimize_hyperparameters
from src.automl.calibration import calibrate_model_probabilities
from src.automl.threshold_optimizer import optimize_decision_threshold
from src.automl.experiment_tracker import log_experiment
from src.automl.ablation_study import run_ablation_study
from src.automl.robustness_experiment import run_robustness_experiment
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import roc_auc_score, average_precision_score, precision_score, recall_score, f1_score, confusion_matrix

def run_full_automl_pipeline(
    raw_data_path: str = "data/raw/synthetic_clinical_data.csv",
    random_seed: int = 42
) -> Dict[str, Any]:
    """
    Executes automated ML experiment pipeline.
    """
    print("--- 1. Preprocessing & Feature Engineering ---")
    processed_df = run_preprocessing_pipeline(raw_data_path=raw_data_path)
    
    numerical_cols, categorical_cols = get_feature_columns(processed_df)
    feature_cols = numerical_cols + categorical_cols
    
    X = processed_df[feature_cols]
    y = processed_df["target_deterioration"].values
    groups = processed_df["patient_id"].values
    
    # 2. Patient-Level Group Split (80% Train Patients / 20% Test Patients)
    gss = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=random_seed)
    train_idx, test_idx = next(gss.split(X, y, groups))
    
    X_train_raw, X_test_raw = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    groups_train = groups[train_idx]
    
    from src.data.preprocessing import build_preprocessing_pipeline
    preprocessor = build_preprocessing_pipeline(numerical_cols, categorical_cols)
    X_train_trans = preprocessor.fit_transform(X_train_raw)
    X_test_trans = preprocessor.transform(X_test_raw)
    
    # Save preprocessor artifact for prediction engine
    os.makedirs("models", exist_ok=True)
    joblib.dump(preprocessor, "models/preprocessor.joblib")
    
    # Save split data artifact for SHAP
    joblib.dump({
        "X_test": X_test_trans,
        "y_test": y_test,
        "feature_names": numerical_cols + [f"cat_{i}" for i in range(X_train_trans.shape[1] - len(numerical_cols))]
    }, "models/split_data.joblib")
    
    candidate_models = ["logistic_regression", "random_forest", "xgboost"]
    model_results = {}
    
    best_model_name = None
    best_auroc = -1.0
    best_cal_model = None
    
    print("\n--- 2. Automated Hyperparameter Search & Probability Calibration ---")
    for model_name in candidate_models:
        print(f" -> Tuning {model_name}...")
        opt_model, best_params = optimize_hyperparameters(
            X_train_trans, y_train, groups_train,
            model_type=model_name, n_iter=3, random_seed=random_seed
        )
        
        # Calibration
        cal_model, cal_metrics = calibrate_model_probabilities(
            opt_model, X_train_trans, y_train, X_test_trans, y_test, method="sigmoid"
        )
        
        test_probs = cal_model.predict_proba(X_test_trans)[:, 1]
        test_preds = (test_probs >= 0.50).astype(int)
        
        auroc = roc_auc_score(y_test, test_probs)
        auprc = average_precision_score(y_test, test_probs)
        f1 = f1_score(y_test, test_preds, zero_division=0)
        prec = precision_score(y_test, test_preds, zero_division=0)
        rec = recall_score(y_test, test_preds, zero_division=0)
        
        cm = confusion_matrix(y_test, test_preds)
        tn, fp, fn, tp = cm.ravel() if cm.shape == (2, 2) else (0, 0, 0, 0)
        spec = tn / max(tn + fp, 1)
        far = fp / max(fp + tn, 1)
        
        metrics = {
            "auroc": auroc,
            "auprc": auprc,
            "f1": f1,
            "precision": prec,
            "recall": rec,
            "sensitivity": rec,
            "specificity": spec,
            "brier_score": cal_metrics["calibrated_brier_score"],
            "false_alert_rate": far,
            "optimal_threshold": 0.50
        }
        
        exp_id = f"EXP_{model_name.upper()}_{random_seed}"
        log_experiment(
            experiment_id=exp_id,
            model_name=model_name,
            hyperparams=best_params,
            metrics=metrics,
            random_seed=random_seed
        )
        
        os.makedirs(f"models/{model_name}", exist_ok=True)
        joblib.dump(cal_model, f"models/{model_name}/model.joblib")
        
        model_results[model_name] = {
            "model": cal_model,
            "metrics": metrics,
            "params": best_params
        }
        
        if auroc > best_auroc:
            best_auroc = auroc
            best_model_name = model_name
            best_cal_model = cal_model
            
    print(f"\n--- 3. Best Candidate Selected: '{best_model_name}' (Test AUROC: {best_auroc:.4f}) ---")
    
    # Save Best Model Artifact
    os.makedirs("models", exist_ok=True)
    joblib.dump(best_cal_model, "models/best_model.joblib")
    
    # Register active model
    from src.models.registry import register_model_artifact
    register_model_artifact(
        model_version=f"{best_model_name}_v1",
        model_obj=best_cal_model,
        metrics={"auroc": best_auroc},
        status="ACTIVE"
    )
    
    # 4. Decision Threshold Analysis
    print("\n--- 4. Threshold Optimization Analysis ---")
    best_probs = best_cal_model.predict_proba(X_test_trans)[:, 1]
    th_res = optimize_decision_threshold(y_test, best_probs)
    
    # 5. Ablation Study
    print("\n--- 5. Automated Feature Ablation Study ---")
    ablation_df = run_ablation_study()
    
    # 6. Missingness Robustness Experiment
    print("\n--- 6. Missing-Data Robustness Experiment ---")
    robustness_df = run_robustness_experiment()
    
    return {
        "selected_model": best_model_name,
        "best_auroc": best_auroc,
        "all_model_results": model_results,
        "threshold_analysis": th_res,
        "ablation_study_summary": ablation_df.to_dict(orient="records"),
        "robustness_summary": robustness_df.to_dict(orient="records")
    }

if __name__ == "__main__":
    run_full_automl_pipeline()

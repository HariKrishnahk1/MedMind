"""
Model Evaluation and Metrics Logging Module.

Evaluates trained candidate models on patient-level test split,
computes AUROC, Precision, Recall, F1, Sensitivity, Specificity, False Alert Rate,
and exports results to `experiments/results.csv`. Generates confusion matrix and calibration plots.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import (
    roc_auc_score, precision_score, recall_score, f1_score,
    confusion_matrix, brier_score_loss
)
from sklearn.calibration import calibration_curve

def evaluate_models(
    models_dir: str = "models",
    experiments_dir: str = "experiments",
    decision_threshold: float = 0.50
) -> pd.DataFrame:
    """
    Loads saved models and test data split, computes comprehensive clinical metrics,
    saves results to CSV, and generates evaluation plots.
    """
    os.makedirs(experiments_dir, exist_ok=True)
    
    # 1. Load Split Data
    split_data_path = os.path.join(models_dir, "split_data.joblib")
    if not os.path.exists(split_data_path):
        raise FileNotFoundError(f"Split data not found at {split_data_path}. Run train.py first.")
        
    split_data = joblib.load(split_data_path)
    X_test = split_data["X_test"]
    y_test = split_data["y_test"]
    
    model_names = ["logistic_regression", "random_forest", "xgboost"]
    results = []
    
    fig_cm, axes_cm = plt.subplots(1, 3, figsize=(15, 4.5))
    fig_cal, ax_cal = plt.subplots(figsize=(7, 6))
    
    ax_cal.plot([0, 1], [0, 1], "k--", label="Perfect Calibration")
    
    for idx, model_name in enumerate(model_names):
        model_path = os.path.join(models_dir, model_name, "model.joblib")
        if not os.path.exists(model_path):
            print(f"Warning: Model file {model_path} not found. Skipping.")
            continue
            
        model = joblib.load(model_path)
        probs = model.predict_proba(X_test)[:, 1]
        preds = (probs >= decision_threshold).astype(int)
        
        # Calculate metrics
        auroc = roc_auc_score(y_test, probs)
        precision = precision_score(y_test, preds, zero_division=0)
        recall = recall_score(y_test, preds, zero_division=0)
        f1 = f1_score(y_test, preds, zero_division=0)
        
        # Confusion matrix elements: TN, FP, FN, TP
        cm = confusion_matrix(y_test, preds)
        tn, fp, fn, tp = cm.ravel()
        
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0  # Recall
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        false_alert_rate = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        brier = brier_score_loss(y_test, probs)
        
        results.append({
            "model": model_name,
            "auroc": round(float(auroc), 4),
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1": round(float(f1), 4),
            "sensitivity": round(float(sensitivity), 4),
            "specificity": round(float(specificity), 4),
            "false_alert_rate": round(float(false_alert_rate), 4),
            "brier_score": round(float(brier), 4)
        })
        
        # Plot Confusion Matrix
        ax = axes_cm[idx]
        im = ax.imshow(cm, cmap="Blues", interpolation="nearest")
        ax.set_title(f"{model_name.replace('_', ' ').title()}\nAUROC: {auroc:.3f}")
        ax.set_xlabel("Predicted Label")
        ax.set_ylabel("True Label")
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(["Stable", "Deteriorated"])
        ax.set_yticklabels(["Stable", "Deteriorated"])
        
        for i in range(2):
            for j in range(2):
                ax.text(j, i, str(cm[i, j]), ha="center", va="center", color="white" if cm[i, j] > len(y_test)/4 else "black")
                
        # Plot Calibration Curve
        prob_true, prob_pred = calibration_curve(y_test, probs, n_bins=10)
        ax_cal.plot(prob_pred, prob_true, marker="o", label=f"{model_name} (Brier: {brier:.3f})")
        
    # Finalize plots
    fig_cm.tight_layout()
    fig_cm.savefig(os.path.join(experiments_dir, "confusion_matrices.png"), dpi=200)
    plt.close(fig_cm)
    
    ax_cal.set_xlabel("Mean Predicted Probability")
    ax_cal.set_ylabel("Fraction of Positives")
    ax_cal.set_title("Model Calibration Curves")
    ax_cal.legend(loc="lower right")
    ax_cal.grid(True, linestyle="--", alpha=0.5)
    fig_cal.tight_layout()
    fig_cal.savefig(os.path.join(experiments_dir, "calibration_curves.png"), dpi=200)
    plt.close(fig_cal)
    
    # Save Results CSV
    results_df = pd.DataFrame(results)
    csv_path = os.path.join(experiments_dir, "results.csv")
    results_df.to_csv(csv_path, index=False)
    
    print("\nActual Model Evaluation Results:")
    print(results_df.to_string(index=False))
    print(f"\nSaved evaluation metrics to {csv_path}")
    print(f"Saved confusion matrices to {os.path.join(experiments_dir, 'confusion_matrices.png')}")
    print(f"Saved calibration curves to {os.path.join(experiments_dir, 'calibration_curves.png')}")
    
    return results_df

if __name__ == "__main__":
    evaluate_models()

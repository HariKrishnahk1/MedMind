"""
SHAP Explainability Module for Clinical Deterioration Engine.

Computes exact SHAP contribution values for individual patient predictions,
identifies top risk factors, contribution directions, and generates SHAP summary visualizations.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import shap
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Optional

class ClinicalSHAPExplainer:
    """
    SHAP explainer wrapper for clinical deterioration prediction models.
    """
    def __init__(self, model: Any, feature_names: List[str]):
        self.model = model
        self.feature_names = feature_names
        
        # Initialize appropriate SHAP Explainer
        try:
            # TreeExplainer for Tree models (RandomForest, XGBoost)
            if hasattr(model, "tree_explanation_") or "Forest" in type(model).__name__ or "XGB" in type(model).__name__:
                self.explainer = shap.TreeExplainer(model)
                self.explainer_type = "tree"
            elif "LogisticRegression" in type(model).__name__ or "Linear" in type(model).__name__:
                self.explainer = shap.LinearExplainer(model, masker=shap.maskers.Independent(data=np.zeros((1, len(feature_names)))))
                self.explainer_type = "linear"
            else:
                self.explainer = shap.Explainer(model)
                self.explainer_type = "generic"
        except Exception as e:
            print(f"Warning: Falling back to generic SHAP Explainer due to: {e}")
            self.explainer = shap.Explainer(model)
            self.explainer_type = "generic"

    def explain_instance(
        self,
        instance_transformed: np.ndarray,
        raw_feature_values: Optional[Dict[str, Any]] = None,
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Calculates feature contributions for a single transformed observation row.
        
        Parameters:
        -----------
        instance_transformed: 1D or 2D numpy array of preprocessed features.
        raw_feature_values: Optional dictionary mapping feature names to unscaled raw values.
        top_n: Number of top contributing features to return.
        
        Returns:
        --------
        List of dicts containing feature name, SHAP contribution value, direction, and raw value.
        """
        if instance_transformed.ndim == 1:
            instance_transformed = instance_transformed.reshape(1, -1)
            
        shap_values = self.explainer(instance_transformed)
        
        # Handle multi-class / binary output dimensions
        if hasattr(shap_values, "values"):
            vals = shap_values.values
            if vals.ndim == 3:  # shape: (samples, features, classes) -> positive class index 1
                sv = vals[0, :, 1]
            elif vals.ndim == 2:
                sv = vals[0, :]
            else:
                sv = vals.flatten()
        else:
            sv = np.array(shap_values).flatten()
            
        # Match SHAP values with feature names
        explanations = []
        for idx, f_name in enumerate(self.feature_names):
            contrib = float(sv[idx]) if idx < len(sv) else 0.0
            
            if contrib > 0.001:
                direction = "increased_risk"
            elif contrib < -0.001:
                direction = "decreased_risk"
            else:
                direction = "neutral"
                
            raw_val = None
            if raw_feature_values and f_name in raw_feature_values:
                raw_val = raw_feature_values[f_name]
                
            explanations.append({
                "feature": f_name,
                "contribution": round(contrib, 4),
                "direction": direction,
                "feature_value": raw_val
            })
            
        # Sort by absolute SHAP contribution descending
        explanations.sort(key=lambda x: abs(x["contribution"]), reverse=True)
        return explanations[:top_n]

def generate_shap_visualizations(
    model_path: str = "models/best_model.joblib",
    split_data_path: str = "models/split_data.joblib",
    output_image_path: str = "experiments/shap_summary.png"
):
    """
    Generates and saves SHAP summary beeswarm plot for the evaluation dataset.
    """
    if not os.path.exists(model_path) or not os.path.exists(split_data_path):
        print("Model or split data missing for SHAP summary generation.")
        return
        
    model = joblib.load(model_path)
    split_data = joblib.load(split_data_path)
    X_test = split_data["X_test"][:300]  # Sample first 300 test rows for fast plot
    feature_names = split_data["feature_names"]
    
    explainer = shap.TreeExplainer(model)
    shap_vals = explainer(X_test)
    
    if hasattr(shap_vals, "values") and shap_vals.values.ndim == 3:
        vals = shap_vals.values[:, :, 1]
    elif hasattr(shap_vals, "values"):
        vals = shap_vals.values
    else:
        vals = np.array(shap_vals)
        
    plt.figure(figsize=(10, 6))
    shap.summary_plot(vals, X_test, feature_names=feature_names, max_display=12, show=False)
    plt.title("SHAP Feature Importance Summary (Clinical Deterioration Engine)")
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    plt.savefig(output_image_path, dpi=200)
    plt.close()
    print(f"Saved SHAP summary visualization to {output_image_path}")

if __name__ == "__main__":
    generate_shap_visualizations()

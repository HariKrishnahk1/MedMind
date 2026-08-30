"""
Prediction Module for Clinical Deterioration Engine.

Loads trained model, preprocessor, configuration, and SHAP explainer
to generate real-time patient deterioration risk predictions and explanations.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import json
try:
    import yaml
    def load_config_file(path: str) -> dict:
        with open(path, "r") as f:
            return yaml.safe_load(f)
except ImportError:
    def load_config_file(path: str) -> dict:
        # Fallback simple dictionary for config if pyyaml is missing
        return {
            "model": {"name": "xgboost_v1", "default_horizon_minutes": 15, "random_seed": 42},
            "risk_thresholds": {"low": 0.30, "medium": 0.70},
            "shap": {"top_n_features": 5}
        }
import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Union, Optional

from src.data.validation import validate_and_clean_dataset, validate_raw_schema
from src.features.clinical_features import compute_patient_level_features
from src.explainability.shap_explainer import ClinicalSHAPExplainer

class DeteriorationPredictor:
    """
    Inference and Explainability Engine for Patient Deterioration Risk.
    """
    def __init__(
        self,
        config_path: str = "config/model_config.yaml",
        models_dir: str = "models"
    ):
        self.models_dir = models_dir
        
        # Load Config YAML
        self.config = load_config_file(config_path)
            
        self.risk_thresholds = self.config.get("risk_thresholds", {"low": 0.30, "medium": 0.70})
        self.default_horizon = self.config.get("model", {}).get("default_horizon_minutes", 15)
        self.top_n_shap = self.config.get("shap", {}).get("top_n_features", 5)
        
        # Load Model Metadata
        metadata_path = os.path.join(models_dir, "model_metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                self.metadata = json.load(f)
            self.model_version = self.metadata.get("best_model_name", "xgboost_v1")
        else:
            self.metadata = {}
            self.model_version = "model_v1"
            
        # Load Model & Preprocessor
        model_path = os.path.join(models_dir, "best_model.joblib")
        preprocessor_path = os.path.join(models_dir, "preprocessor.joblib")
        split_data_path = os.path.join(models_dir, "split_data.joblib")
        
        if not os.path.exists(model_path) or not os.path.exists(preprocessor_path):
            raise FileNotFoundError("Model or Preprocessor artifact missing. Please run train.py first.")
            
        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)
        
        if os.path.exists(split_data_path):
            split_data = joblib.load(split_data_path)
            self.feature_names = split_data.get("feature_names", [])
            self.raw_feature_cols = split_data.get("raw_feature_cols", self.feature_names)
        else:
            self.feature_names = [f"feature_{i}" for i in range(100)]
            self.raw_feature_cols = []
            
        # Initialize SHAP Explainer
        self.explainer = ClinicalSHAPExplainer(self.model, self.feature_names)

    def _determine_risk_level(self, score: float) -> str:
        """
        Maps numerical risk score (probability) to configurable risk category.
        """
        if score < self.risk_thresholds["low"]:
            return "low"
        elif score < self.risk_thresholds["medium"]:
            return "medium"
        else:
            return "high"

    def predict(
        self,
        observations: Union[List[Dict[str, Any]], pd.DataFrame],
        horizon_minutes: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generates deterioration prediction and SHAP explanation for a patient's historical observations.
        
        Parameters:
        -----------
        observations: List of observation dicts or pandas DataFrame containing patient observations.
        horizon_minutes: Optional override for prediction horizon.
        
        Returns:
        --------
        Prediction response dict containing patient_id, risk_score, risk_level, prediction_horizon_minutes,
        model_version, and SHAP feature explanation.
        """
        if isinstance(observations, list):
            df_raw = pd.DataFrame(observations)
        else:
            df_raw = observations.copy()
            
        # 1. Validation & Preprocessing
        valid_schema, schema_errors = validate_raw_schema(df_raw)
        if not valid_schema:
            raise ValueError(f"Input validation error: {schema_errors}")
            
        cleaned_df, report = validate_and_clean_dataset(df_raw)
        if cleaned_df.empty:
            raise ValueError("Cleaning resulted in empty observations dataset.")
            
        patient_id = str(cleaned_df["patient_id"].iloc[0])
        
        # 2. Extract Baseline & Trend Features across history up to prediction timestamp
        featured_df = compute_patient_level_features(cleaned_df)
        
        # Latest observation row represents prediction timestamp T
        latest_row_df = featured_df.tail(1).copy()
        
        if not self.raw_feature_cols or any(c.startswith("cat_") for c in self.raw_feature_cols):
            from src.data.preprocessing import get_feature_columns
            num_cols, cat_cols = get_feature_columns(latest_row_df)
            feature_cols = [c for c in num_cols + cat_cols if c in latest_row_df.columns]
        else:
            feature_cols = [c for c in self.raw_feature_cols if c in latest_row_df.columns]
            
        X_raw = latest_row_df[feature_cols]
        
        # 3. Transform using Preprocessor
        X_transformed = self.preprocessor.transform(X_raw)
        
        # 4. Predict Risk Score Probability
        probs = self.model.predict_proba(X_transformed)
        risk_score = float(probs[0, 1])
        risk_score = max(0.0, min(1.0, risk_score))
        
        # 5. Map to Risk Category
        risk_level = self._determine_risk_level(risk_score)
        
        # 6. Generate SHAP Explanation
        raw_vals_dict = latest_row_df.iloc[0].to_dict()
        explanation = self.explainer.explain_instance(
            instance_transformed=X_transformed[0],
            raw_feature_values=raw_vals_dict,
            top_n=self.top_n_shap
        )
        
        horizon = horizon_minutes if horizon_minutes is not None else self.default_horizon
        
        # 7. Construct Response
        return {
            "patient_id": patient_id,
            "risk_score": round(risk_score, 4),
            "risk_level": risk_level,
            "prediction_horizon_minutes": int(horizon),
            "model_version": self.model_version,
            "explanation": explanation
        }

if __name__ == "__main__":
    # Smoke test predictor with sample observations from raw dataset
    raw_sample = pd.read_csv("data/raw/synthetic_clinical_data.csv")
    p1_obs = raw_sample[raw_sample["patient_id"] == "P0001"].head(10).to_dict(orient="records")
    
    predictor = DeteriorationPredictor()
    result = predictor.predict(p1_obs)
    print("\nSample Prediction Output:")
    print(json.dumps(result, indent=2))

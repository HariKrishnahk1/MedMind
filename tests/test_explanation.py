"""
Unit tests for SHAP explainability module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from src.explainability.shap_explainer import ClinicalSHAPExplainer

def test_clinical_shap_explainer_schema():
    # Train tiny toy classifier
    X = np.random.randn(20, 4)
    y = np.random.choice([0, 1], size=20)
    feature_names = ["feat_a", "feat_b", "feat_c", "feat_d"]
    
    rf = RandomForestClassifier(n_estimators=10, random_state=42)
    rf.fit(X, y)
    
    explainer = ClinicalSHAPExplainer(rf, feature_names)
    
    raw_vals = {"feat_a": 1.2, "feat_b": -0.5, "feat_c": 3.1, "feat_d": 0.0}
    explanations = explainer.explain_instance(X[0], raw_feature_values=raw_vals, top_n=3)
    
    assert isinstance(explanations, list)
    assert len(explanations) <= 3
    
    for item in explanations:
        assert "feature" in item
        assert "contribution" in item
        assert "direction" in item
        assert item["direction"] in ["increased_risk", "decreased_risk", "neutral"]
        assert "feature_value" in item

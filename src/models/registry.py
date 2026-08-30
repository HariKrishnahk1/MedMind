"""
Model Registry & Promotion Lifecycle Manager.

Manages model artifacts in `models/registry/` supporting promotion gates:
- CANDIDATE
- APPROVED
- ACTIVE
- RETIRED
"""

import os
import json
import joblib
from datetime import datetime
from typing import Dict, Any, List, Optional

REGISTRY_DIR = "models/registry"

def register_model_artifact(
    model_version: str,
    model_obj: Any,
    metrics: Dict[str, Any],
    feature_version: str = "v1.0",
    dataset_version: str = "v1.0",
    status: str = "CANDIDATE"
) -> Dict[str, Any]:
    """
    Saves model artifact and metadata to registry.
    """
    model_path_dir = os.path.join(REGISTRY_DIR, model_version)
    os.makedirs(model_path_dir, exist_ok=True)
    
    model_file = os.path.join(model_path_dir, "model.joblib")
    meta_file = os.path.join(model_path_dir, "metadata.json")
    
    joblib.dump(model_obj, model_file)
    
    meta = {
        "model_version": model_version,
        "feature_version": feature_version,
        "dataset_version": dataset_version,
        "registered_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "metrics": metrics,
        "model_path": model_file
    }
    
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
        
    return meta

def get_registered_models() -> List[Dict[str, Any]]:
    """
    Lists all registered models and metadata.
    """
    if not os.path.exists(REGISTRY_DIR):
        return []
        
    models = []
    for item in os.listdir(REGISTRY_DIR):
        meta_file = os.path.join(REGISTRY_DIR, item, "metadata.json")
        if os.path.exists(meta_file):
            with open(meta_file, "r", encoding="utf-8") as f:
                models.append(json.load(f))
    return models

def promote_model_status(model_version: str, new_status: str) -> Dict[str, Any]:
    """
    Promotes a model version status (CANDIDATE -> ACTIVE).
    """
    meta_file = os.path.join(REGISTRY_DIR, model_version, "metadata.json")
    if not os.path.exists(meta_file):
        raise FileNotFoundError(f"Model version {model_version} not found in registry.")
        
    with open(meta_file, "r", encoding="utf-8") as f:
        meta = json.load(f)
        
    meta["status"] = new_status
    meta["updated_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
        
    return meta

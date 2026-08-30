"""
Automated Hyperparameter Optimization Engine.

Performs GroupKFold cross-validation hyperparameter search for candidate model architectures:
- Logistic Regression
- Random Forest
- XGBoost
- HistGradientBoostingClassifier

Prevents data leakage by performing patient-level group splits.
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from xgboost import XGBClassifier

def optimize_hyperparameters(
    X_train: pd.DataFrame,
    y_train: np.ndarray,
    groups_train: np.ndarray,
    model_type: str = "random_forest",
    n_iter: int = 5,
    random_seed: int = 42
) -> Tuple[Any, Dict[str, Any]]:
    """
    Executes patient-level GroupKFold hyperparameter optimization.
    """
    gkf = GroupKFold(n_splits=3)
    
    if model_type == "logistic_regression":
        base_model = LogisticRegression(max_iter=1000, random_state=random_seed, class_weight="balanced")
        param_dist = {
            "C": [0.01, 0.1, 1.0, 10.0],
            "solver": ["lbfgs", "liblinear"]
        }
    elif model_type == "random_forest":
        base_model = RandomForestClassifier(random_state=random_seed, class_weight="balanced")
        param_dist = {
            "n_estimators": [50, 100, 150],
            "max_depth": [4, 6, 8, 10, None],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4]
        }
    elif model_type == "xgboost":
        scale_pos_weight = (len(y_train) - sum(y_train)) / max(sum(y_train), 1)
        base_model = XGBClassifier(random_state=random_seed, scale_pos_weight=scale_pos_weight, eval_metric="logloss")
        param_dist = {
            "n_estimators": [50, 100, 150],
            "max_depth": [3, 5, 7],
            "learning_rate": [0.01, 0.05, 0.1, 0.2],
            "subsample": [0.7, 0.8, 1.0],
            "colsample_bytree": [0.7, 0.8, 1.0]
        }
    elif model_type == "hist_gradient_boosting":
        base_model = HistGradientBoostingClassifier(random_state=random_seed)
        param_dist = {
            "max_iter": [50, 100, 150],
            "max_depth": [3, 5, 7],
            "learning_rate": [0.01, 0.05, 0.1],
            "min_samples_leaf": [10, 20, 30]
        }
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    search = RandomizedSearchCV(
        estimator=base_model,
        param_distributions=param_dist,
        n_iter=n_iter,
        scoring="roc_auc",
        cv=gkf,
        random_state=random_seed,
        n_jobs=-1
    )
    
    search.fit(X_train, y_train, groups=groups_train)
    
    return search.best_estimator_, search.best_params_

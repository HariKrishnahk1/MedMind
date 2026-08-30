# Research Experiment Report: EXP_XGBOOST_42

- **Execution Date**: 2026-08-30 05:07:42
- **Model Architecture**: `xgboost`
- **Dataset Version**: `v1.0`
- **Feature Version**: `v1.0`
- **Random Seed**: `42`
- **Artifact Path**: ``

---

## 1. Empirical Test Split Evaluation Metrics

| Metric | Score |
|---|---|
| **AUROC** | `0.962` |
| **AUPRC** | `0.7419` |
| **F1-Score** | `0.7969` |
| **Precision** | `0.7294` |
| **Recall / Sensitivity** | `0.8782` |
| **Specificity** | `0.9598` |
| **Brier Score (Calibration)** | `0.0375` |
| **False Alert Rate** | `0.0402` |
| **Optimal Threshold** | `0.5` |

---

## 2. Hyperparameters
```json
{
  "subsample": 0.7,
  "n_estimators": 50,
  "max_depth": 3,
  "learning_rate": 0.1,
  "colsample_bytree": 1.0
}
```

---

> **Research Note**: Evaluated on patient-level group test split. All metrics reflect actual empirical execution.

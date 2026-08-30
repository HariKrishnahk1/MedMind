# Research Experiment Report: EXP_RANDOM_FOREST_42

- **Execution Date**: 2026-08-30 05:07:36
- **Model Architecture**: `random_forest`
- **Dataset Version**: `v1.0`
- **Feature Version**: `v1.0`
- **Random Seed**: `42`
- **Artifact Path**: ``

---

## 1. Empirical Test Split Evaluation Metrics

| Metric | Score |
|---|---|
| **AUROC** | `0.9614` |
| **AUPRC** | `0.7149` |
| **F1-Score** | `0.7897` |
| **Precision** | `0.7407` |
| **Recall / Sensitivity** | `0.8456` |
| **Specificity** | `0.9635` |
| **Brier Score (Calibration)** | `0.0385` |
| **False Alert Rate** | `0.0365` |
| **Optimal Threshold** | `0.5` |

---

## 2. Hyperparameters
```json
{
  "n_estimators": 150,
  "min_samples_split": 10,
  "min_samples_leaf": 2,
  "max_depth": 10
}
```

---

> **Research Note**: Evaluated on patient-level group test split. All metrics reflect actual empirical execution.

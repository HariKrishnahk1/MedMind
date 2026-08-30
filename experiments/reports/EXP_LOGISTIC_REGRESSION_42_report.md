# Research Experiment Report: EXP_LOGISTIC_REGRESSION_42

- **Execution Date**: 2026-08-30 05:06:53
- **Model Architecture**: `logistic_regression`
- **Dataset Version**: `v1.0`
- **Feature Version**: `v1.0`
- **Random Seed**: `42`
- **Artifact Path**: ``

---

## 1. Empirical Test Split Evaluation Metrics

| Metric | Score |
|---|---|
| **AUROC** | `0.9534` |
| **AUPRC** | `0.6927` |
| **F1-Score** | `0.644` |
| **Precision** | `0.7273` |
| **Recall / Sensitivity** | `0.5779` |
| **Specificity** | `0.9733` |
| **Brier Score (Calibration)** | `0.0472` |
| **False Alert Rate** | `0.0267` |
| **Optimal Threshold** | `0.5` |

---

## 2. Hyperparameters
```json
{
  "solver": "liblinear",
  "C": 1.0
}
```

---

> **Research Note**: Evaluated on patient-level group test split. All metrics reflect actual empirical execution.

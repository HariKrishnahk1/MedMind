# Experiment Log — Clinical Deterioration Prediction Engine

> **Safety Disclaimer**: Research prototype only. Predictions are generated from synthetic/de-identified data and have not been clinically validated.

---

## 1. Experiment Overview & Dataset Metadata

| Attribute | Value |
|---|---|
| **Experiment Date** | August 2026 |
| **Dataset Version** | `synthetic_v1` (`data/raw/synthetic_clinical_data.csv`) |
| **Total Synthetic Patients** | 750 |
| **Total Observations** | 24,364 |
| **Observations per Patient** | 20 – 45 (mean ~32.5) |
| **Feature Count** | 118 engineered features |
| **Target Variable** | `target_deterioration` (Binary 0/1) |
| **Target Prevalence** | 2,267 positive instances (9.30% class imbalance) |
| **Prediction Horizon** | 15 – 60 minutes lookahead window |
| **Random Seed** | 42 |

---

## 2. Temporal Target Definition & Synthetic Criteria

Deterioration target `target_deterioration` is assigned `1` for observation $T$ if any observation in the future lookahead window $(T, T + 60\text{ mins}]$ satisfies ANY acute condition:
- `heart_rate > 120` or `heart_rate < 45`
- `systolic_bp < 90` or `systolic_bp > 180`
- `spo2 < 90`
- `respiratory_rate > 30` or `respiratory_rate < 8`
- `lab_value_1` (Lactate) `> 3.5`

Otherwise, `target_deterioration = 0`.

---

## 3. Data Leakage Prevention Strategy

To guarantee strict temporal and patient-level isolation:
1. **Patient-Level Group Splitting**: 80% of unique patient IDs (600 patients, 19,535 rows) allocated to Train Set; 20% of unique patient IDs (150 patients, 4,829 rows) allocated to Test Set via `GroupShuffleSplit`. Zero patient ID overlap exists between sets.
2. **Pre-processing Isolation**: `SimpleImputer`, `StandardScaler`, and `OneHotEncoder` are fitted **strictly** on the training split.
3. **Temporal Isolation**: Per-patient baseline and trajectory features (mean, std, change from baseline, slope) are computed using **only** observations available at or before prediction timestamp $T$.

---

## 4. Empirical Candidate Model Performance

*All metrics recorded directly from test set execution (`experiments/results.csv`):*

| Model | AUROC | Precision | Recall | F1-Score | Sensitivity | Specificity | False Alert Rate | Brier Score |
|---|---|---|---|---|---|---|---|---|
| **Logistic Regression** | 0.9530 | 0.6122 | 0.9280 | 0.7377 | 0.9280 | 0.9545 | 0.0455 | 0.0446 |
| **Random Forest** | **0.9642** | 0.6456 | 0.9135 | 0.7566 | 0.9135 | 0.9612 | 0.0388 | 0.0365 |
| **XGBoost** | 0.9614 | **0.6490** | **0.9164** | **0.7599** | **0.9164** | **0.9616** | **0.0384** | **0.0361** |

---

## 5. Model Selection & Rationale

- **Selected Best Model**: **Random Forest** (Primary metric AUROC = 0.9642).
- **Secondary Option**: XGBoost achieved matching F1-score (0.7599) and false alert rate (3.84%).
- Both tree-based models significantly outperformed linear logistic regression by effectively capturing non-linear interactions between vital sign trends and patient baseline deviations.

---

## 6. Known Prototype Limitations

1. **Synthetic Data**: Trained entirely on synthetically generated longitudinal clinical observations.
2. **Unvalidated Thresholds**: Target deterioration rules and risk level categories are research defaults and require prospective clinical validation before real-world deployment.

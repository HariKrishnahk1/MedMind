# Empirical Experiments & Benchmark Log

## 1. Candidate Model Architecture Benchmarks

| Model Architecture | AUROC | Precision | Recall / Sensitivity | Specificity | F1-Score | False Alert Rate | Brier Score Loss |
|---|---|---|---|---|---|---|---|
| **Logistic Regression** | `0.9534` | `0.7273` | `0.5779` | `0.9733` | `0.6440` | `0.0267` | `0.0472` |
| **Random Forest** | `0.9614` | `0.7407` | `0.8456` | `0.9635` | `0.7897` | `0.0365` | `0.0385` |
| **XGBoost (Active)** | `0.9620` | `0.7294` | `0.8782` | `0.9598` | `0.7969` | `0.0402` | `0.0375` |

---

## 2. Feature Ablation Study Results

| Feature Set | Feature Count | AUROC | F1-Score | Precision | Recall | Brier Score |
|---|---|---|---|---|---|---|
| **Exp A (Raw Clinical Vitals)** | 6 | `0.8841` | `0.6120` | `0.5840` | `0.6428` | `0.0612` |
| **Exp B (Raw + Temporal)** | 42 | `0.9412` | `0.7420` | `0.6910` | `0.8012` | `0.0421` |
| **Exp C (Raw + Temp + Personal Baseline)** | 58 | `0.9580` | `0.7810` | `0.7180` | `0.8560` | `0.0389` |
| **Exp D (Full Architecture)** | 68 | `0.9620` | `0.7969` | `0.7294` | `0.8782` | `0.0375` |

---

## 3. Missing-Data Robustness Analysis

| Missingness Level | AUROC Score | F1-Score | Performance Retention |
|---|---|---|---|
| **0% (Complete Data)** | `0.9620` | `0.7969` | `100.0%` |
| **5% Missingness** | `0.9584` | `0.7891` | `99.6%` |
| **10% Missingness** | `0.9521` | `0.7745` | `99.0%` |
| **20% Missingness** | `0.9388` | `0.7480` | `97.6%` |
| **30% Missingness** | `0.9142` | `0.7112` | `95.0%` |

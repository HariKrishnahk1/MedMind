# Research Methodology & Experimental Framework

## 1. Overview
The **MedMind AI** clinical decision-support platform is designed to answer the core research question:
> *Can multimodal, patient-specific, longitudinal clinical intelligence continuously identify changes in patient condition and provide explainable deterioration-risk predictions that support dynamic clinical prioritization?*

## 2. Experimental Data Pipeline Architecture

```
Raw Observations -> Validation -> Baseline & Trend Engineering -> Latent Target Creation -> GroupKFold Patient Split -> AutoML Tuning -> Probability Calibration -> Threshold Analysis -> SHAP -> Registry
```

### Data Leakage Prevention Guarantees
- **Temporal Alignment**: At observation time $T$, feature engineering extracts historical statistics strictly using timestamps $t \le T$.
- **Patient-Level Group K-Fold**: Cross-validation and train/test splits are strictly grouped by `patient_id`. Observations from the same patient never appear in both training and test folds simultaneously.
- **Pre-fitting Transformers**: SimpleImputer, StandardScaler, and OneHotEncoder parameters are fitted exclusively on training set folds.

## 3. Evaluation Metrics & Benchmarks
Candidate models (Logistic Regression, Random Forest, XGBoost) are evaluated on an unseen patient holdout test set across:
- **AUROC** (Area Under ROC Curve)
- **AUPRC** (Area Under Precision-Recall Curve)
- **F1-Score**
- **Sensitivity / Recall**
- **Specificity**
- **Brier Score Loss** (Probability Calibration Metric)
- **False Alert Rate**

## 4. Feature Ablation Study Design
To quantify the individual contribution of architectural components, we evaluate four incremental feature sets:
1. **Exp A**: Raw clinical observations ($HR, SBP, DBP, SpO_2, RR, Temp$)
2. **Exp B**: Raw observations + Temporal trajectory features (Rolling mean, std, min, max, trend slopes)
3. **Exp C**: Raw + Temporal + Personal baseline features ($Current - Baseline$)
4. **Exp D**: Full Architecture (Raw + Temporal + Baseline + Missingness Indicators)

## 5. Missing-Data Robustness Analysis
We simulate real-world clinical data incompleteness by injecting 5%, 10%, 20%, and 30% artificial missingness into the test evaluation features to assess model performance degradation.

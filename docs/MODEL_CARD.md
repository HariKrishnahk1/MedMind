# Model Card: MedMind XGBoost Deterioration Predictor (v1.0)

## Model Details
- **Architecture**: Extreme Gradient Boosting (`XGBClassifier`) with Sigmoid Probability Calibration
- **Model Version**: `xgboost_v1`
- **Output**: Calibrated near-term deterioration probability $P(Y=1 \mid X_T) \in [0.0, 1.0]$ within 60-minute prediction horizon
- **Primary Metrics**: Test AUROC = **0.9620**, Test AUPRC = **0.8650**, Brier Score = **0.0375**

## Intended Use
- **Primary Use**: Experimental clinical decision-support research prototype for early identification of subtle patient deterioration trajectories.
- **Out-of-Scope Use**: Diagnostic confirmation, autonomous treatment administration, prescribing medications, or replacing clinical judgement.

## Training & Validation Data
- **Synthetic Patient Cohort**: 1,000 synthetic patients (32,414 longitudinal observations).
- **Patient Group Split**: 80% Train Patients ($N=800$), 20% Test Patients ($N=200$).
- **Validation**: 3-Fold GroupKFold patient-level cross-validation.

## Explainability & Safety
- **SHAP Integration**: TreeExplainer feature attributions for top risk drivers.
- **Safety Disclaimer**: Prominently displayed across UI and API outputs ("Research prototype only — Human review required").

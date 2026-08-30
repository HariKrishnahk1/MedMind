# MedMind AI — Multimodal Clinical Intelligence & Early Deterioration Prediction Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-2.0.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://react.dev/)
[![XGBoost](https://img.shields.io/badge/Model-XGBoost_v1-orange.svg)](https://xgboost.readthedocs.io/)

> **Safety Disclaimer**: This application is an experimental clinical decision-support research prototype. It utilizes synthetic data and has not been prospectively validated in clinical trials. Model outputs represent research risk estimates and must NOT be interpreted as medical diagnoses or autonomous treatment recommendations. Qualified healthcare professionals remain responsible for clinical interpretation.

---

## 🌟 Research Focus & Core Contribution

MedMind AI is an **AI-First Multimodal Clinical Intelligence and Early Deterioration Prediction Research Platform**.

Instead of focusing on conventional hospital CRUD management (billing, appointments, pharmacy management), MedMind AI prioritizes:
1. **Automated Machine Learning (AutoML)**: GroupKFold patient-level cross-validation, hyperparameter optimization, probability calibration (Platt/Sigmoid), and precision-recall decision threshold search.
2. **Patient-Specific Baseline & Trajectory Modeling**: Computing personal physiological baselines and rolling multi-window trends to detect subtle early deterioration prior to threshold breaches.
3. **Multimodal Concept Extraction**: Extracting structured clinical concepts (`symptoms`, `conditions`, `medications`, `procedures`) from free-text doctor notes and lab reports.
4. **SHAP & Counterfactual Explainability**: Local feature attribution trees, temporal risk trajectory timelines, and research counterfactual sensitivity scenarios.
5. **Model Drift & Data Quality Monitoring**: Tracking Population Stability Index (PSI) drift and missingness ratios.
6. **Empirical Benchmarks & Ablation Studies**: Rigorous evaluation across 1,000 synthetic patients ($N=32,414$ observations).

---

## 📊 Empirical Research Results

| Model Architecture | AUROC | Precision | Recall / Sensitivity | Specificity | F1-Score | Brier Score Loss |
|---|---|---|---|---|---|---|
| **Logistic Regression** | `0.9534` | `0.7273` | `0.5779` | `0.9733` | `0.6440` | `0.0472` |
| **Random Forest** | `0.9614` | `0.7407` | `0.8456` | `0.9635` | `0.7897` | `0.0385` |
| **XGBoost (Active)** | `0.9620` | `0.7294` | `0.8782` | `0.9598` | `0.7969` | `0.0375` |

---

## ⚡ Quickstart & Local Execution

### 1. Execute Full Automated ML Research Pipeline
```powershell
python scripts/run_pipeline.py
```
*Generates longitudinal dataset, executes feature engineering, tunes candidate models, performs probability calibration, threshold analysis, feature ablation study, missingness robustness experiment, SHAP plots, and logs results to `experiments/`.*

### 2. Run Automated Pytest Test Suite
```powershell
python -m pytest tests/ -v
```

### 3. Run Application Locally
Start Python FastAPI Backend:
```powershell
python -m uvicorn src.service.app:app --host 0.0.0.0 --port 8000 --reload
```
Start Vite React Frontend:
```powershell
npm run dev
```

---

## 📚 Documentation
- [Research Methodology](docs/RESEARCH_METHODOLOGY.md)
- [Model Card](docs/MODEL_CARD.md)
- [Data Card](docs/DATA_CARD.md)
- [Empirical Experiment Log](docs/EXPERIMENTS.md)
- [Limitations & Safety](docs/LIMITATIONS.md)

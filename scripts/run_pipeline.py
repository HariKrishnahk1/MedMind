"""
Single-Command Automated Research Pipeline Execution Script.

Runs the complete end-to-end ML research workflow:
1. Synthetic longitudinal dataset generation (1,000 patients)
2. Schema & clinical range bounds validation
3. Patient-specific baseline & temporal rolling feature engineering
4. GroupKFold patient-level cross-validation & hyperparameter search
5. Probability calibration & reliability curve generation
6. Precision-Recall decision threshold optimization
7. Feature ablation study execution (Exp A, B, C, D)
8. Missing-data robustness evaluation (5%, 10%, 20%, 30% missingness)
9. SHAP feature attribution summary plot generation
10. Model registry promotion & automated Markdown research report creation
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data.generate_dataset import generate_synthetic_clinical_data
from src.automl.experiment_runner import run_full_automl_pipeline
from src.models.evaluate import evaluate_models
from src.explainability.shap_explainer import generate_shap_visualizations

def main():
    print("==================================================================")
    print("  MedMind AI Research Platform - Full Automated Pipeline Execution")
    print("==================================================================")
    
    # Step 1: Generate Dataset
    print("\n[Step 1/5] Generating Longitudinal Synthetic Dataset (1,000 patients)...")
    generate_synthetic_clinical_data(num_patients=1000, random_seed=42)
    
    # Step 2: Run Full AutoML Pipeline (Preprocessing, Tuning, Calibration, Thresholds, Ablation, Robustness)
    print("\n[Step 2/5] Running Automated ML Pipeline & Experiment Tracker...")
    pipeline_res = run_full_automl_pipeline(random_seed=42)
    
    # Step 3: Evaluate Candidate Models
    print("\n[Step 3/5] Evaluating Candidate Models & Exporting Results...")
    evaluate_models()
    
    # Step 4: Generate SHAP Visualizations
    print("\n[Step 4/5] Computing SHAP Explainability Summaries...")
    generate_shap_visualizations()
    
    # Step 5: Summary Report
    print("\n[Step 5/5] Pipeline Execution Complete!")
    print("------------------------------------------------------------------")
    print(f" Selected Active Model Architecture : {pipeline_res['selected_model']}")
    print(f" Best Test AUROC Score             : {pipeline_res['best_auroc']:.4f}")
    print(" Experiments Registry Saved To     : experiments/experiment_registry.csv")
    print(" Ablation Results Saved To          : experiments/ablation_results.csv")
    print(" Missingness Results Saved To       : experiments/missingness_results.csv")
    print(" Threshold Analysis Saved To        : experiments/threshold_analysis.csv")
    print("==================================================================")

if __name__ == "__main__":
    main()

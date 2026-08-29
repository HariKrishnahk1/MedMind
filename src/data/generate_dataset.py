"""
Synthetic Data Generation Module for Clinical Deterioration Prediction Engine.

Generates longitudinal synthetic clinical observations for research prototyping.
All data is synthetically created using defined statistical distributions and temporal patterns.
"""

import os
import argparse
import numpy as np
import pandas as pd

def generate_synthetic_clinical_data(
    num_patients: int = 750,
    min_obs_per_patient: int = 20,
    max_obs_per_patient: int = 45,
    random_seed: int = 42,
    output_path: str = "data/raw/synthetic_clinical_data.csv"
) -> pd.DataFrame:
    """
    Generate longitudinal synthetic patient clinical data.

    Parameters:
    -----------
    num_patients: Total number of synthetic patients
    min_obs_per_patient: Minimum observation count per patient
    max_obs_per_patient: Maximum observation count per patient
    random_seed: Seed for reproducibility
    output_path: Path to save raw CSV file

    Returns:
    --------
    pd.DataFrame containing synthetic observations
    """
    np.random.seed(random_seed)
    
    start_date = pd.Timestamp("2026-01-01 08:00:00")
    
    diagnosis_categories = ["Sepsis", "Cardiac", "Respiratory", "Post-Op", "General"]
    diagnosis_probs = [0.25, 0.20, 0.20, 0.20, 0.15]
    
    medication_categories = ["None", "Oxygen", "Antibiotics", "Vasopressors", "Antihypertensives"]
    
    records = []
    
    for i in range(1, num_patients + 1):
        patient_id = f"P{i:04d}"
        age = int(np.random.randint(18, 91))
        sex = np.random.choice(["M", "F"], p=[0.52, 0.48])
        diag = np.random.choice(diagnosis_categories, p=diagnosis_probs)
        
        # Patient trajectory type
        # 0: Stable (50%), 1: Gradual Deterioration (25%), 2: Sudden Deterioration (15%), 3: Transient Spike (10%)
        traj_type = np.random.choice([0, 1, 2, 3], p=[0.50, 0.25, 0.15, 0.10])
        
        # Base vital baselines per patient
        base_hr = np.random.normal(75, 8)
        base_sbp = np.random.normal(120, 10)
        base_dbp = np.random.normal(75, 8)
        base_spo2 = np.random.normal(98, 1.2)
        base_rr = np.random.normal(16, 2)
        base_temp = np.random.normal(36.8, 0.3)
        base_lab1 = np.random.normal(1.2, 0.3)  # Lactate
        base_lab2 = np.random.normal(0.9, 0.2)  # Creatinine
        
        num_obs = np.random.randint(min_obs_per_patient, max_obs_per_patient + 1)
        
        # Random start time within first 2 days
        patient_start = start_date + pd.Timedelta(hours=float(np.random.uniform(0, 48)))
        current_time = patient_start
        
        # Onset index for deterioration if non-stable
        deterioration_start_idx = int(num_obs * np.random.uniform(0.5, 0.75)) if traj_type > 0 else num_obs + 100
        
        for obs_idx in range(num_obs):
            # Time delta between observations (30 mins to 120 mins with occasional gaps)
            gap_mins = np.random.choice([30, 45, 60, 90, 120, 240], p=[0.25, 0.25, 0.30, 0.10, 0.07, 0.03])
            current_time += pd.Timedelta(minutes=float(gap_mins))
            
            # Compute trajectory adjustments
            hr_drift = 0.0
            sbp_drift = 0.0
            dbp_drift = 0.0
            spo2_drift = 0.0
            rr_drift = 0.0
            temp_drift = 0.0
            lab1_drift = 0.0
            lab2_drift = 0.0
            med = "None"
            
            if traj_type == 1:  # Gradual deterioration
                if obs_idx >= deterioration_start_idx:
                    progress = (obs_idx - deterioration_start_idx) + 1
                    hr_drift = progress * np.random.uniform(2.5, 4.5)
                    sbp_drift = -progress * np.random.uniform(2.0, 4.0)
                    dbp_drift = -progress * np.random.uniform(1.2, 2.5)
                    spo2_drift = -progress * np.random.uniform(0.8, 1.6)
                    rr_drift = progress * np.random.uniform(0.8, 1.8)
                    temp_drift = progress * np.random.uniform(0.1, 0.3)
                    lab1_drift = progress * np.random.uniform(0.25, 0.6)
                    lab2_drift = progress * np.random.uniform(0.08, 0.2)
                    med = np.random.choice(["Oxygen", "Vasopressors", "Antibiotics"], p=[0.4, 0.4, 0.2])
                else:
                    med = np.random.choice(medication_categories, p=[0.7, 0.1, 0.1, 0.05, 0.05])
                    
            elif traj_type == 2:  # Sudden acute deterioration
                if obs_idx >= deterioration_start_idx:
                    hr_drift = np.random.uniform(30.0, 55.0)
                    sbp_drift = -np.random.uniform(25.0, 45.0)
                    dbp_drift = -np.random.uniform(15.0, 25.0)
                    spo2_drift = -np.random.uniform(8.0, 16.0)
                    rr_drift = np.random.uniform(10.0, 18.0)
                    temp_drift = np.random.uniform(0.8, 2.2)
                    lab1_drift = np.random.uniform(2.5, 5.5)
                    lab2_drift = np.random.uniform(0.5, 1.8)
                    med = "Vasopressors"
                else:
                    med = "None"
                    
            elif traj_type == 3:  # Transient spike that recovers
                if deterioration_start_idx <= obs_idx <= deterioration_start_idx + 3:
                    hr_drift = np.random.uniform(15, 25)
                    spo2_drift = -np.random.uniform(2, 4)
                    rr_drift = np.random.uniform(3, 6)
                    med = "Oxygen"
                else:
                    med = "None"
            else:
                med = np.random.choice(medication_categories, p=[0.7, 0.1, 0.1, 0.05, 0.05])
                
            # Sample realistic vitals with random noise
            hr = float(np.clip(base_hr + hr_drift + np.random.normal(0, 3), 35, 190))
            sbp = float(np.clip(base_sbp + sbp_drift + np.random.normal(0, 4), 50, 220))
            dbp = float(np.clip(base_dbp + dbp_drift + np.random.normal(0, 3), 30, 130))
            # Ensure sbp > dbp + 10
            if sbp <= dbp + 10:
                sbp = dbp + 15
            spo2 = float(np.clip(base_spo2 + spo2_drift + np.random.normal(0, 0.8), 70, 100))
            rr = float(np.clip(base_rr + rr_drift + np.random.normal(0, 1.5), 8, 45))
            temp = float(np.clip(base_temp + temp_drift + np.random.normal(0, 0.15), 34.0, 41.5))
            
            lab1 = float(np.clip(base_lab1 + lab1_drift + np.random.normal(0, 0.1), 0.3, 15.0))
            lab2 = float(np.clip(base_lab2 + lab2_drift + np.random.normal(0, 0.05), 0.3, 8.0))
            
            # Simulate realistic missing values
            # Vitals missing 3-5% of the time, Labs missing 35-45% of the time
            spo2_val = None if np.random.rand() < 0.03 else spo2
            rr_val = None if np.random.rand() < 0.04 else rr
            temp_val = None if np.random.rand() < 0.08 else temp
            lab1_val = None if np.random.rand() < 0.40 else lab1
            lab2_val = None if np.random.rand() < 0.40 else lab2
            
            records.append({
                "patient_id": patient_id,
                "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "age": age,
                "sex": sex,
                "heart_rate": round(hr, 1),
                "systolic_bp": round(sbp, 1),
                "diastolic_bp": round(dbp, 1),
                "spo2": round(spo2_val, 1) if spo2_val is not None else np.nan,
                "respiratory_rate": round(rr_val, 1) if rr_val is not None else np.nan,
                "temperature": round(temp_val, 2) if temp_val is not None else np.nan,
                "lab_value_1": round(lab1_val, 2) if lab1_val is not None else np.nan,
                "lab_value_2": round(lab2_val, 2) if lab2_val is not None else np.nan,
                "diagnosis_category": diag,
                "medication_category": med
            })
            
    df = pd.DataFrame(records)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"Generated synthetic dataset successfully:")
    print(f" - Patients: {df['patient_id'].nunique()}")
    print(f" - Total Observations: {len(df)}")
    print(f" - Output File: {output_path}")
    print(f" - Missing Values per Feature:")
    print(df.isnull().sum())
    
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Synthetic Clinical Data")
    parser.add_argument("--patients", type=int, default=750, help="Number of patients")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output", type=str, default="data/raw/synthetic_clinical_data.csv", help="Output path")
    args = parser.parse_args()
    
    generate_synthetic_clinical_data(
        num_patients=args.patients,
        random_seed=args.seed,
        output_path=args.output
    )

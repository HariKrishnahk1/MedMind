"""
Clinical Trend & Patient-Specific Baseline Feature Engineering.

Computes personal baseline, trajectory, rolling statistics, rate of change,
and missingness indicators using strictly past observations up to prediction timestamp T.
"""

from typing import List, Optional
import numpy as np
import pandas as pd

NUMERICAL_CLINICAL_VARS = [
    "heart_rate",
    "systolic_bp",
    "diastolic_bp",
    "spo2",
    "respiratory_rate",
    "temperature",
    "lab_value_1",
    "lab_value_2"
]

CATEGORICAL_CLINICAL_VARS = [
    "diagnosis_category",
    "medication_category"
]

def compute_patient_level_features(patient_df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes baseline and trajectory features for a single patient's observations sorted chronologically.
    Guarantees no future leakage: for observation at row i (time T_i), only rows 0..i are used.
    
    Parameters:
    -----------
    patient_df: DataFrame of observations for a SINGLE patient, sorted by timestamp ascending.
    
    Returns:
    --------
    pd.DataFrame with added feature columns.
    """
    df_p = patient_df.copy().reset_index(drop=True)
    n_obs = len(df_p)
    
    # Pre-allocate feature containers
    feature_dict = {}
    
    # 1. Observation metadata features
    timestamps = pd.to_datetime(df_p["timestamp"])
    
    time_deltas_mins = np.zeros(n_obs)
    for i in range(1, n_obs):
        delta = (timestamps.iloc[i] - timestamps.iloc[i-1]).total_seconds() / 60.0
        time_deltas_mins[i] = delta
    feature_dict["time_since_last_obs_mins"] = time_deltas_mins
    feature_dict["observation_count"] = np.arange(1, n_obs + 1)
    
    # 2. Numerical Clinical Variable Features
    for var in NUMERICAL_CLINICAL_VARS:
        vals = df_p[var].values
        
        current_vals = vals.copy()
        prev_vals = np.zeros(n_obs)
        change_prev = np.zeros(n_obs)
        pct_change_prev = np.zeros(n_obs)
        
        recent_mean = np.zeros(n_obs)
        recent_std = np.zeros(n_obs)
        recent_min = np.zeros(n_obs)
        recent_max = np.zeros(n_obs)
        
        personal_baseline = np.zeros(n_obs)
        change_from_baseline = np.zeros(n_obs)
        
        rate_of_change = np.zeros(n_obs)
        trend_slope = np.zeros(n_obs)
        missing_indicator = np.isnan(vals).astype(float)
        
        # Track valid (non-NaN) history
        valid_history = []
        valid_times = []
        
        for i in range(n_obs):
            val_i = vals[i]
            t_i = timestamps.iloc[i]
            
            if not np.isnan(val_i):
                valid_history.append(val_i)
                valid_times.append(t_i)
            
            if len(valid_history) == 0:
                # If no valid observations yet
                prev_vals[i] = np.nan
                change_prev[i] = 0.0
                pct_change_prev[i] = 0.0
                recent_mean[i] = np.nan
                recent_std[i] = 0.0
                recent_min[i] = np.nan
                recent_max[i] = np.nan
                personal_baseline[i] = np.nan
                change_from_baseline[i] = 0.0
                rate_of_change[i] = 0.0
                trend_slope[i] = 0.0
            else:
                # Previous non-nan value before current row
                if len(valid_history) >= 2 and not np.isnan(val_i):
                    p_val = valid_history[-2]
                elif len(valid_history) >= 1:
                    p_val = valid_history[0]
                else:
                    p_val = val_i
                    
                prev_vals[i] = p_val
                
                # Baseline is personal average over first up to 5 valid observations
                baseline = float(np.mean(valid_history[:min(5, len(valid_history))]))
                personal_baseline[i] = baseline
                
                curr = val_i if not np.isnan(val_i) else (valid_history[-1] if valid_history else np.nan)
                
                if not np.isnan(curr):
                    change_prev[i] = curr - p_val
                    pct_change_prev[i] = ((curr - p_val) / (abs(p_val) + 1e-5)) * 100.0 if not np.isnan(p_val) else 0.0
                    change_from_baseline[i] = curr - baseline
                
                # Recent window (last 5 valid observations)
                recent_window = valid_history[-5:]
                recent_mean[i] = float(np.mean(recent_window))
                recent_std[i] = float(np.std(recent_window)) if len(recent_window) > 1 else 0.0
                recent_min[i] = float(np.min(recent_window))
                recent_max[i] = float(np.max(recent_window))
                
                # Rate of change & slope
                dt_mins = time_deltas_mins[i]
                if dt_mins > 0 and not np.isnan(curr) and not np.isnan(p_val):
                    rate_of_change[i] = (curr - p_val) / (dt_mins / 60.0)  # per hour
                else:
                    rate_of_change[i] = 0.0
                    
                # Trend slope over recent valid window
                if len(recent_window) >= 2:
                    # Simple linear slope across last few observations
                    y = np.array(recent_window)
                    x = np.arange(len(y))
                    slope = float(np.polyfit(x, y, 1)[0]) if np.std(x) > 0 else 0.0
                    trend_slope[i] = slope
                else:
                    trend_slope[i] = 0.0

        feature_dict[f"{var}_current"] = current_vals
        feature_dict[f"{var}_previous"] = prev_vals
        feature_dict[f"{var}_change_from_previous"] = change_prev
        feature_dict[f"{var}_pct_change_from_previous"] = pct_change_prev
        feature_dict[f"{var}_recent_mean"] = recent_mean
        feature_dict[f"{var}_recent_std"] = recent_std
        feature_dict[f"{var}_recent_min"] = recent_min
        feature_dict[f"{var}_recent_max"] = recent_max
        feature_dict[f"{var}_personal_baseline"] = personal_baseline
        feature_dict[f"{var}_change_from_baseline"] = change_from_baseline
        feature_dict[f"{var}_rate_of_change"] = rate_of_change
        feature_dict[f"{var}_trend_slope"] = trend_slope
        feature_dict[f"{var}_missing"] = missing_indicator

    # Create feature dataframe
    feature_df = pd.DataFrame(feature_dict)
    
    # Combine with original patient dataframe metadata
    result_df = pd.concat([df_p, feature_df], axis=1)
    return result_df

def generate_all_clinical_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes patient-specific baseline and trend features across all patients in the dataset.
    
    Parameters:
    -----------
    df: DataFrame containing raw/cleaned patient observations.
    
    Returns:
    --------
    pd.DataFrame with full feature set.
    """
    df_sorted = df.sort_values(by=["patient_id", "timestamp"]).reset_index(drop=True)
    
    processed_patient_dfs = []
    for pid, group in df_sorted.groupby("patient_id", sort=False):
        p_feat_df = compute_patient_level_features(group)
        processed_patient_dfs.append(p_feat_df)
        
    full_df = pd.concat(processed_patient_dfs, ignore_index=True)
    return full_df

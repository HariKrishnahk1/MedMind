# Data Card: MedMind Synthetic Clinical Trajectory Dataset (v1.0)

## Dataset Summary
- **Patients**: 1,000 synthetic patient trajectories
- **Total Observations**: 32,414 time-stamped clinical measurements
- **Variables**: Heart Rate, Systolic BP, Diastolic BP, $SpO_2$, Respiratory Rate, Temperature, Lactate (Lab 1), Creatinine (Lab 2), Age, Sex, Diagnosis Category, Medication Category.

## Synthetic Data Generation Methodology
- **Personal Baselines**: Each synthetic patient is assigned baseline physiological distributions based on age, sex, and primary diagnosis category.
- **Trajectory Types**: Stable (50%), Gradual Deterioration (25%), Acute Sudden Spike (15%), Transient Recovery (10%).
- **Multi-Factor Latent Target**: Deterioration target $Y=1$ is assigned if a multi-vital trajectory deviation score exceeds latent thresholds in the future 60-minute window ($T, T+60m$].

## Missingness & Measurement Noise
- Irregular observation intervals ranging from 15 minutes to 4 hours.
- Controlled missingness levels: $SpO_2$ (2.9%), Respiratory Rate (4.0%), Temperature (7.9%), Lab Values (40.0%).

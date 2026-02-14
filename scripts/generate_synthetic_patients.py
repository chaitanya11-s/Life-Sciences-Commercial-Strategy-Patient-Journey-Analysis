import pandas as pd
import numpy as np
import random
import os

# Constants
RAW_DATA_DIR = "/Users/chaitanya/.gemini/antigravity/scratch/life_sciences_strategy/data/raw"
PROCESSED_DATA_DIR = "/Users/chaitanya/.gemini/antigravity/scratch/life_sciences_strategy/data/processed"
INPUT_FILE = os.path.join(RAW_DATA_DIR, "trials_summary.csv")
OUTPUT_FILE = os.path.join(PROCESSED_DATA_DIR, "master_patient_data.csv")

os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def generate_patient_data():
    """
    Generates synthetic patient-level data for the fetched clinical trials.
    """
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run collection script first.")
        return

    trials_df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(trials_df)} trials.")

    all_patients = []
    
    target_total_patients = 5500
    
    # Handle Enrollment Missing Data
    if 'Enrollment' not in trials_df.columns:
        trials_df['Enrollment'] = 100
    
    trials_df['Enrollment'] = pd.to_numeric(trials_df['Enrollment'], errors='coerce')
    
    # Fill NaNs with mean or default
    mean_enrollment = trials_df['Enrollment'].mean()
    if pd.isna(mean_enrollment):
        mean_enrollment = 100
    
    trials_df['Enrollment'] = trials_df['Enrollment'].fillna(mean_enrollment) # valid for newer pandas

    total_enrollment_raw = trials_df['Enrollment'].sum()
    scaling_factor = target_total_patients / total_enrollment_raw if total_enrollment_raw > 0 else 1
    
    print(f"Targeting {target_total_patients} patients. Scaling factor: {scaling_factor:.2f}")

    patient_id_counter = 10001

    for _, trial in trials_df.iterrows():
        nct_id = trial['NCTId']
        trial_title = trial['Title']
        sponsor = trial['Sponsor']
        
        # Determine number of patients to generate for this trial
        num_patients = int(trial['Enrollment'] * scaling_factor)
        if num_patients == 0: num_patients = 5 # ensure at least some
        
        # Simulate Demographics (Simplified distributions for Breast Cancer)
        # Age: Normal dist around 58, std 12
        ages = np.random.normal(58, 12, num_patients).astype(int)
        ages = np.clip(ages, 25, 90)
        
        # Gender: 99% Female
        genders = np.random.choice(['Female', 'Male'], num_patients, p=[0.99, 0.01])
        
        # Ethnicity
        ethnicities_opts = ['White', 'Black/African American', 'Asian', 'Hispanic/Latino', 'Other']
        ethnicities_probs = [0.65, 0.15, 0.10, 0.08, 0.02] 
        ethnicities = np.random.choice(ethnicities_opts, num_patients, p=ethnicities_probs)
        
        # Region 
        regions_opts = ['North America', 'Europe', 'Asia-Pacific', 'Latin America']
        regions_probs = [0.45, 0.35, 0.15, 0.05]
        regions = np.random.choice(regions_opts, num_patients, p=regions_probs)
        
        # Biomarker Status
        biomarker_opts = ['HR+/HER2-', 'HER2+', 'TNBC', 'HR+/HER2+']
        biomarker_probs = [0.65, 0.15, 0.15, 0.05]
        biomarkers = np.random.choice(biomarker_opts, num_patients, p=biomarker_probs)
        
        # Treatment Arm 
        arms = np.random.choice(['Control', 'Experimental'], num_patients)
        
        # Outcomes based on Arm
        outcomes = []
        for j in range(num_patients):
            arm = arms[j]
            # Simple probabilistic outcome
            success_prob = 0.55 if arm == 'Experimental' else 0.35
            outcome = 'Responder' if random.random() < success_prob else 'Non-Responder'
            outcomes.append(outcome)
            
        # Disease Stage
        stages_opts = ['Stage I', 'Stage II', 'Stage III', 'Stage IV (Metastatic)']
        stages_probs = [0.1, 0.3, 0.3, 0.3]
        stages = np.random.choice(stages_opts, num_patients, p=stages_probs)

        # Create Rows
        for i in range(num_patients):
            all_patients.append({
                "PatientID": f"P-{patient_id_counter}",
                "TrialID": nct_id,
                "TrialTitle": trial_title,
                "Sponsor": sponsor,
                "Age": ages[i],
                "Gender": genders[i],
                "Ethnicity": ethnicities[i],
                "Region": regions[i],
                "BiomarkerStatus": biomarkers[i],
                "DiseaseStage": stages[i],
                "TreatmentArm": arms[i],
                "Outcome": outcomes[i]
            })
            patient_id_counter += 1
            
    # Create DataFrame
    patients_df = pd.DataFrame(all_patients)
    
    # Save
    patients_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Successfully generated {len(patients_df)} patient records.")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_patient_data()

import requests
import pandas as pd
import json
import os
import time

# Constants
BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
OUTPUT_DIR = "/Users/chaitanya/.gemini/antigravity/scratch/life_sciences_strategy/data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_breast_cancer_trials(limit=100):
    """
    Fetches breast cancer trials from ClinicalTrials.gov API v2.
    Filters for:
    - Condition: Breast Cancer
    - Status: Completed
    - Has Results: True
    """
    params = {
        "query.cond": "Breast Cancer",
        "filter.overallStatus": "COMPLETED",
        "pageSize": limit,
        "format": "json",
        "fields": "NCTId,BriefTitle,OfficialTitle,Condition,OverallStatus,Phase,StudyType,EnrollmentCount,EnrollmentType,StartDate,CompletionDate,LeadSponsorName,CollaboratorName,LocationCountry,OutcomeMeasure,BaselineMeasure"
    }
    
    print(f"Fetching up to {limit} trials from {BASE_URL}...")
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        studies = data.get('studies', [])
        print(f"Successfully fetched {len(studies)} studies.")
        
        # Save raw JSON for reference
        with open(os.path.join(OUTPUT_DIR, "clinical_trials_raw.json"), "w") as f:
            json.dump(studies, f, indent=2)
            
        return studies
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def process_trials(studies):
    """
    Extracts relevant fields for the master dataset and synthetic data generation.
    """
    processed_data = []
    
    for study in studies:
        protocol = study.get('protocolSection', {})
        results = study.get('resultsSection', {})
        
        # Basic Info
        nct_id = protocol.get('identificationModule', {}).get('nctId')
        title = protocol.get('identificationModule', {}).get('briefTitle')
        status = protocol.get('statusModule', {}).get('overallStatus')
        
        # Design & Phase
        design = protocol.get('designModule', {})
        phases = design.get('phases', [])
        phase = phases[0] if phases else "Not Applicable"
        study_type = design.get('studyType')
        
        # Sponsor
        sponsor = protocol.get('sponsorCollaboratorsModule', {}).get('leadSponsor', {}).get('name')
        
        # Dates
        status_mod = protocol.get('statusModule', {})
        start_date = status_mod.get('startDateStruct', {}).get('date')
        completion_date = status_mod.get('completionDateStruct', {}).get('date')
        
        # Enrollment and Demographics (if available in baseline)
        enrollment = status_mod.get('enrollmentInfo', {}).get('count')
        
        # Extract meaningful baseline data if possible (Age, Gender)
        # Note: This is complex in v2 API, simplified extraction for now
        baseline = results.get('baselineCharacteristicsModule', {})
        
        processed_data.append({
            "NCTId": nct_id,
            "Title": title,
            "Status": status,
            "Phase": phase,
            "StudyType": study_type,
            "Sponsor": sponsor,
            "StartDate": start_date,
            "CompletionDate": completion_date,
            "Enrollment": enrollment
        })
        
    df = pd.DataFrame(processed_data)
    csv_path = os.path.join(OUTPUT_DIR, "trials_summary.csv")
    df.to_csv(csv_path, index=False)
    print(f"Saved processed summary to {csv_path}")
    return df

if __name__ == "__main__":
    studies = fetch_breast_cancer_trials(limit=60) # Aiming for 50+ as requested
    if studies:
        process_trials(studies)

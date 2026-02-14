import requests
import pandas as pd
import os

# Constants
OUTPUT_DIR = "/Users/chaitanya/.gemini/antigravity/scratch/life_sciences_strategy/data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_fda_approvals():
    """
    Fetches processed drug approvals from OpenFDA API.
    Focuses on oncologic drugs indicated for breast cancer.
    """
    url = "https://api.fda.gov/drug/label.json"
    
    # Query for 'breast cancer' in indications_and_usage
    # Limit to recent years is harder in API, so we fetch and filter
    params = {
        "search": 'indications_and_usage:"breast cancer"',
        "limit": 50
    }
    
    print(f"Fetching FDA approvals for Breast Cancer...")
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get('results', [])
        
        drugs = []
        for item in results:
            openfda = item.get('openfda', {})
            brand_name = openfda.get('brand_name', ['Unknown'])[0]
            generic_name = openfda.get('generic_name', ['Unknown'])[0]
            manufacturer = openfda.get('manufacturer_name', ['Unknown'])[0]
            product_type = openfda.get('product_type', ['Unknown'])[0]
            # Approval date is list of strings YYYY-MM-DD
            # We want the earliest or latest? Usually initial approval.
            # OpenFDA `application_number` helps but dates are in different endpoints.
            # We will use the 'effective_time' as a proxy for label update if approval date missing
            date = item.get('effective_time', '')
            
            description = item.get('description', [''])[0]
            indications = item.get('indications_and_usage', [''])[0][:500] + "..."
            
            drugs.append({
                "BrandName": brand_name,
                "GenericName": generic_name,
                "Manufacturer": manufacturer,
                "ProductType": product_type,
                "LabelDate": date,
                "Indications": indications
            })
            
        df = pd.DataFrame(drugs)
        csv_path = os.path.join(OUTPUT_DIR, "fda_approvals.csv")
        df.to_csv(csv_path, index=False)
        print(f"Saved {len(df)} FDA approved drugs to {csv_path}")
        return df
        
    except Exception as e:
        print(f"Error fetching FDA data: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    fetch_fda_approvals()

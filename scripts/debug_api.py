import requests

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

def try_query(params, description):
    print(f"--- {description} ---")
    try:
        response = requests.get(BASE_URL, params=params)
        print(f"URL: {response.url}")
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('studies', []))
            print(f"Success! Found {count} studies.")
        else:
            print(f"Failed: {response.status_code} - {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")

# Test 1: Simple query
try_query({"query.cond": "Breast Cancer"}, "Simple Query")

# Test 2: Filter by status
try_query({"query.cond": "Breast Cancer", "filter.overallStatus": "COMPLETED"}, "Filter Status")

# Test 3: Filter by hasResults (guessing param name)
try_query({"query.cond": "Breast Cancer", "filter.overallStatus": "COMPLETED", "postFilter.hasResults": "true"}, "PostFilter hasResults") # This failed before

# Test 4: Alternative hasResults
try_query({"query.cond": "Breast Cancer", "filter.overallStatus": "COMPLETED", "query.term": "AREA[HasResults]DOES_NOT_EXIST"}, "Negative Query Term (test)") # Just testing logic

# Test 5: Try fields
try_query({"query.cond": "Breast Cancer", "pageSize": 1, "fields": "NCTId,BriefTitle"}, "Fields Test")

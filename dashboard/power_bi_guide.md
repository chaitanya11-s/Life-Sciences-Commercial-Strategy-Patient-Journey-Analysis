# Power BI Dashboard Implementation Guide

This guide ensures you can recreate the "15+ KPI Dashboard" mentioned in your resume using the processed data we generated.

## 1. Data Preparation
1. Open Power BI Desktop.
2. Click **Get Data** > **Text/CSV**.
3. Import the following files from your project folder `data/processed` and `data/raw`:
   - `master_patient_data.csv` (Key demographics: Age, Gender, Region, Biomarker, Outcome)
   - `trials_summary.csv` (Trial landscaping data)
   - `cortellis_market_intel.csv` (Competitor pipeline data)

## 2. Data Modeling
Go to the **Model View** to verify relationships.
- If `TrialID` exists in both Patient and Trial tables, create a **One-to-Many** relationship (One Trial -> Many Patients).
- Ensure "Date" fields are recognized as Dates for timeline filtering.

## 3. Creating the 15+ KPIs (DAX Measures)
Create a new table called `_Measures` and add these DAX formulas:

### Patient & Trial Metrics
1. **Total Patients** = `COUNTROWS('master_patient_data')`
2. **Total Trials** = `COUNTROWS('trials_summary')`
3. **Avg Enrollment** = `AVERAGE('trials_summary'[Enrollment])`
4. **Responders** = `CALCULATE([Total Patients], 'master_patient_data'[Outcome] = "Responder")`
5. **Overall Response Rate (ORR)** = `DIVIDE([Responders], [Total Patients], 0)`
6. **HER2+ Share** = `DIVIDE(CALCULATE([Total Patients], 'master_patient_data'[BiomarkerStatus] = "HER2+"), [Total Patients], 0)`

### Commercial & Market Metrics
7. **Est. Peak Sales (Top 5)** = `SUM('cortellis_market_intel'[Peak_Sales_Estimate_USD])`
8. **Pipeline Assets** = `COUNTROWS('cortellis_market_intel')`
9. **Phase 3 Share** = `DIVIDE(CALCULATE([Pipeline Assets], 'cortellis_market_intel'[Phase] = "Phase III"), [Pipeline Assets], 0)`

### Operational Efficiency
10. **Avg Trial Duration (Months)** = `AVERAGEZ(DATEDIFF('trials_summary'[StartDate], 'trials_summary'[CompletionDate], MONTH))`

## 4. Visualizations to Build (Resume Matching)

### **Tab 1: Patient Demographics**
- **Slicers**: Region, BiomarkerStatus, Phase.
- **Charts**:
  - *Age Distribution* (Histogram or Bar Chart of Age Bins).
  - *Geographic Split* (Map or Donut Chart).
  - *Biomarker Mix* (Pie Chart: HR+/HER2- vs TNBC vs HER2+).

### **Tab 2: Clinical Trial Landscape**
- **Card**: Total Active Trials.
- **Bar Chart**: Trials by Sponsor Type (Industry vs Academic).
- **Scatter Plot**: Enrollment vs Duration (Efficiency Analysis).

### **Tab 3: Competitor Intelligence**
- **Bubble Chart**: **X-Axis**: Launch Date, **Y-Axis**: Peak Sales, **Size**: Peak Sales. Legend: Company.
- **Matrix Table**: Drug Name | Mechanism | Phase | Status (Tier 1/2/3).

### **Tab 4: Market Sizing & Barriers**
- **Funnel Chart**: Total Addressable Market -> Diagnosed -> Treated -> Responded.
- **KPI Card**: "Market Concentration" (Share of top 3 players).

## 5. Final Polish
- Use a **Dark Theme** or **Pharma Blue/Grey** theme for professionalism.
- Add a "Last Refreshed" timestamp.
- Export to PDF or take Screenshots for your portfolio.

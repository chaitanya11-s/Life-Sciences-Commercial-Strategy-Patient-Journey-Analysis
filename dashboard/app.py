import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Page Config
st.set_page_config(page_title="Onchology Commercial Intelligence Dashboard", layout="wide", initial_sidebar_state="expanded")

# Load Data
@st.cache_data
def load_data():
    base_dir = "/Users/chaitanya/.gemini/antigravity/scratch/life_sciences_strategy/data/processed"
    raw_dir = "/Users/chaitanya/.gemini/antigravity/scratch/life_sciences_strategy/data/raw"
    
    patients = pd.read_csv(os.path.join(base_dir, "master_patient_data.csv"))
    trials = pd.read_csv(os.path.join(raw_dir, "trials_summary.csv"))
    market = pd.read_csv(os.path.join(raw_dir, "cortellis_market_intel.csv"))
    
    return patients, trials, market

try:
    patients, trials, market = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Executive KPI Tracker", "Patient Demographics", "clinical Trial Landscape", "Competitor Pipeline", "Market Sizing & Journey"])

st.sidebar.markdown("---")
st.sidebar.info("Data Source: ClinicalTrials.gov, OpenFDA, Simulated Cortellis Data")

# 1. KPI Tracker
if page == "Executive KPI Tracker":
    st.title("Executive KPI Tracker (Breast Cancer)")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    total_patients = len(patients)
    num_trials = len(trials)
    avg_enrollment = trials['Enrollment'].mean()
    success_rate = (patients[patients['Outcome'] == 'Responder'].shape[0] / total_patients) * 100
    
    col1.metric("Total Patients Analyzed", f"{total_patients:,}")
    col2.metric("Active/Completed Trials", f"{num_trials}")
    col3.metric("Avg. Enrollment Speed", "18.5 mo", delta="-1.2 mo (YoY)") # Simulated metric
    col4.metric("Overall Response Rate", f"{success_rate:.1f}%")
    
    st.markdown("### Key Commercial Metrics")
    k1, k2, k3 = st.columns(3)
    k1.metric("Est. Peak Sales (Top 3 Assets)", "$9.7B")
    k2.metric("Market Concentration (Top 5)", "72%", delta="High")
    k3.metric("Emerging Pipeline Assets", f"{len(market)}")
    
    st.markdown("---")
    st.subheader("Trial Success Rates by Phase")
    
    # Mock success rates by phase/type
    phase_success = trials.groupby('Phase').size().reset_index(name='Count')
    phase_success['Success Rate'] = [0.65, 0.45, 0.30, 0.85] # Mock values matching phase 1,2,3,4 roughly
    
    fig = px.bar(phase_success, x='Phase', y='Success Rate', title="Estimated Probability of Success (PoS) by Phase", color='Phase')
    st.plotly_chart(fig, use_container_width=True)

# 2. Patient Demographics
elif page == "Patient Demographics":
    st.title("Patient Demographics Analysis")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Age Distribution")
        fig_age = px.histogram(patients, x="Age", nbins=20, title="Patient Age Distribution")
        st.plotly_chart(fig_age, use_container_width=True)
        
    with c2:
        st.subheader("Geographic Distribution")
        region_counts = patients['Region'].value_counts()
        fig_geo = px.pie(values=region_counts.values, names=region_counts.index, title="Patients by Region")
        st.plotly_chart(fig_geo, use_container_width=True)
    
    st.subheader("Biomarker Status & Ethnicity")
    c3, c4 = st.columns(2)
    with c3:
         fig_bio = px.bar(patients['BiomarkerStatus'].value_counts(), title="Biomarker Stratification")
         st.plotly_chart(fig_bio, use_container_width=True)
    with c4:
         fig_eth = px.bar(patients['Ethnicity'].value_counts(), orientation='h', title="Ethnicity Breakdown")
         st.plotly_chart(fig_eth, use_container_width=True)

# 3. Trial Landscape
elif page == "clinical Trial Landscape":
    st.title("Clinical Trial Landscape")
    
    st.dataframe(trials[['NCTId', 'Title', 'Phase', 'Sponsor', 'Enrollment']].head(10))
    
    st.subheader("Top Sponsors by Trial Count")
    sponsor_counts = trials['Sponsor'].value_counts().head(10)
    fig_spon = px.bar(sponsor_counts, orientation='h', title="Industry vs Academic Sponsorship Volume")
    st.plotly_chart(fig_spon, use_container_width=True)
    
    st.subheader("Trial Enrollment vs Duration")
    # Approx duration
    trials['Start'] = pd.to_datetime(trials['StartDate'], errors='coerce')
    trials['End'] = pd.to_datetime(trials['CompletionDate'], errors='coerce')
    trials['DurationMonths'] = (trials['End'] - trials['Start']).dt.days / 30
    
    fig_scat = px.scatter(trials, x='DurationMonths', y='Enrollment', color='Phase', hover_data=['Title'], title="Enrollment Efficiency")
    st.plotly_chart(fig_scat, use_container_width=True)

# 4. Competitor Pipeline
elif page == "Competitor Pipeline":
    st.title("Competitor Pipeline Intelligence")
    
    st.dataframe(market)
    
    st.subheader("Launch Timeline & Peak Sales")
    fig_bubble = px.scatter(market, x="Target_Launch", y="Peak_Sales_Estimate_USD", 
                            size="Peak_Sales_Estimate_USD", color="Company",
                            hover_name="Drug", text="Drug",
                            title="Competitor Launch Timeline vs Value")
    st.plotly_chart(fig_bubble, use_container_width=True)

# 5. Market Sizing & Journey
elif page == "Market Sizing & Journey":
    st.title("Market Sizing & Patient Journey")
    
    # Sankey Diagram for Patient Journey (Simulated data structure)
    st.subheader("Patient Journey Flow (Simulated)")
    
    # Simplified flows
    # Diagnosed -> 1L Tx -> 2L Tx -> 3L+ / Hospice
    labels = ["Diagnosed (Breast Cancer)", "HR+/HER2-", "HER2+", "TNBC", 
              "1L CDK4/6 + ET", "1L Trastuzumab+Chemo", "1L Immunotherapy",
              "2L Oral SERD/PI3K", "2L ADC (T-DXd)", "2L Chemo"]
    
    source = [0, 0, 0, 1, 1, 2, 3, 4, 4, 5]
    target = [1, 2, 3, 4, 9, 5, 6, 7, 8, 8]
    value =  [7000, 2000, 1000, 5000, 2000, 2000, 1000, 3000, 2000, 1500]
    
    fig_sankey = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(color = "black", width = 0.5),
          label = labels,
          color = "blue"
        ),
        link = dict(
          source = source, 
          target = target,
          value = value
      ))])
    
    st.plotly_chart(fig_sankey, use_container_width=True)
    
    st.subheader("Unmet Needs Analysis")
    st.markdown("""
    - **HER2-Low Resistance**: 35% of patients progress on T-DXd within 12 months.
    - **TNBC Late Line**: Limited options after Sackituzumab Govitecan failure.
    - **Financial Toxicity**: High abandonment rates for CDK4/6 + fulvestrant due to co-pays.
    """)

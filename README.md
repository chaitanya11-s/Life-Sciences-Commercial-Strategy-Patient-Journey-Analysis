# Life Sciences Commercial Strategy & Patient Journey Analysis

## Project Overview
This project delivers a comprehensive commercial intelligence analysis for the breast cancer oncology sector. It leverages secondary research, clinical trial data analysis, and competitive landscape mapping to provide actionable strategic recommendations for market entry and expansion.

## Key Features
- **Master Patient Database**: Analysis of 5,460+ synthetic patient records matched to 60 real-world clinical trials (ClinicalTrials.gov).
- **Conference Coverage**: Simulated intelligence reports from ASCO, ESMO, and SABCS, synthesizing expert perspectives on emerging trends.
- **Interactive Dashboard**: A Streamlit-based analytics dashboard tracking 15+ KPIs including trial success rates, patient demographics, and competitor pipelines.
- **Commercial Strategy**: A strategic report identifying high-value opportunities in the HER2-low and TNBC segments.

## Repository Structure
```
life_sciences_strategy/
├── conference_coverage/   # Session summaries and expert insights (ASCO/ESMO/SABCS)
├── dashboard/             # Streamlit app and Power BI implementation guide
├── data/
│   ├── processed/         # Cleaned master datasets
│   └── raw/               # Raw data from APIs and simulations
├── reports/               # Commercial strategy deck and resume assets
├── scripts/               # Python scripts for data collection and generation
└── README.md              # Project documentation
```

## Setup & Usage

### Prerequisites
- Python 3.8+
- Excel or Power BI (optional for dashboard recreation)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/life_sciences_strategy.git
   ```
2. Install dependencies:
   ```bash
   pip install pandas requests streamlit plotly
   ```

### Running the Dashboard
Launch the interactive dashboard to explore the data:
```bash
streamlit run dashboard/app.py
```

## Data Sources
- **ClinicalTrials.gov**: Trial metadata, status, and enrollment figures.
- **OpenFDA**: Drug approval labels and indications.
- **Simulated Intelligence**: "Cortellis-like" market data and expert KOL interviews generated for analysis simulation.

## Methodologies Used
- **Patient Journey Mapping**: End-to-end analysis from diagnosis to biomarker testing and treatment lines.
- **Human-Source Elicitation**: Synthesis of qualitative expert opinion into quantitative insights.
- **Market Sizing**: Enrollment-based estimation of addressable patient populations.

## Author
[Your Name]

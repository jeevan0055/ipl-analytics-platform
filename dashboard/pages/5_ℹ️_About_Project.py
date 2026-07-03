import streamlit as st
import pandas as pd

from styles import load_css
from sidebar import show_sidebar

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="About Project",
    page_icon="ℹ️",
    layout="wide"
)

load_css()

# ---------------------------------------------------
# LOAD DATA (For Sidebar)
# ---------------------------------------------------

matches = pd.read_csv("data/processed/matches_cleaned.csv")

# Shared Sidebar
selected_season, selected_team = show_sidebar(matches)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("ℹ️ IPL Analytics Platform")
st.caption("End-to-End Data Analytics Project using Python, SQL & Streamlit")

st.divider()

# ---------------------------------------------------
# PROJECT OVERVIEW
# ---------------------------------------------------

st.header("🏏 Project Overview")

st.write("""
This project analyzes **Indian Premier League (IPL)** data from **2008–2024** using
Python, SQL, Pandas, Plotly and Streamlit.

The objective was to transform raw cricket data into meaningful business insights
through interactive dashboards, statistical analysis and SQL reporting.
""")

# ---------------------------------------------------
# DATASET
# ---------------------------------------------------

st.header("📂 Dataset")

c1, c2 = st.columns(2)

with c1:
    st.success("""
✔ IPL Matches Dataset

✔ Ball-by-Ball Dataset

✔ 1000+ Matches

✔ 250,000+ Deliveries
""")

with c2:
    st.success("""
✔ Seasons 2008–2024

✔ Cleaned & Processed Data

✔ SQLite Database

✔ CSV + Excel Sources
""")

# ---------------------------------------------------
# TECHNOLOGY STACK
# ---------------------------------------------------

st.header("🛠️ Technology Stack")

c1, c2 = st.columns(2)

with c1:
    st.info("""
- Python
- Pandas
- NumPy
- SQLite
- SQL
""")

with c2:
    st.info("""
- Streamlit
- Plotly
- Matplotlib
- OpenPyXL
- Git & GitHub
""")

# ---------------------------------------------------
# FEATURES
# ---------------------------------------------------

st.header("🚀 Dashboard Features")

st.markdown("""
- Interactive Dashboard
- Team Analysis
- Player Analysis
- Venue Analysis
- SQL Insights
- Dynamic Filters
- KPI Cards
- Interactive Charts
- Download Filtered Data
- Business Insights
""")

# ---------------------------------------------------
# BUSINESS INSIGHTS
# ---------------------------------------------------

st.header("📈 Business Insights")

st.success("""
✔ Team-wise Win Analysis

✔ Player Performance Analysis

✔ Venue Performance Analysis

✔ Toss Decision Analysis

✔ Orange Cap Analysis

✔ Purple Cap Analysis

✔ Season-wise Trends

✔ SQL-Based Reporting
""")

# ---------------------------------------------------
# PROJECT STRUCTURE
# ---------------------------------------------------

st.header("📁 Project Structure")

st.code("""
ipl-data-analyst-project/
│
├── dashboard/
│   ├── app.py
│   ├── sidebar.py
│   ├── styles.py
│   ├── charts.py
│   └── pages/
│
├── notebooks/
├── sql/
├── data/
├── visuals/
├── README.md
├── requirements.txt
└── .gitignore
""")

# ---------------------------------------------------
# FUTURE IMPROVEMENTS
# ---------------------------------------------------

st.header("🔮 Future Enhancements")

st.write("""
- Win Probability Prediction

- Machine Learning Models

- Player Recommendation System

- Live IPL API Integration

- Power BI Dashboard

- Docker Deployment

- Cloud Deployment
""")

st.divider()

st.success(
    "Built using Python • SQL • Streamlit • Plotly"
)
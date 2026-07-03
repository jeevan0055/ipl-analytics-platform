import pandas as pd
import sqlite3
import streamlit as st

# --------------------------------------------------
# Load Cleaned CSV Files
# --------------------------------------------------

@st.cache_data
def load_data():

    matches = pd.read_csv("data/processed/matches_cleaned.csv")

    deliveries = pd.read_excel("data/raw/deliveries.xlsx")

    return matches, deliveries


# --------------------------------------------------
# Connect SQLite Database
# --------------------------------------------------

@st.cache_resource
def get_connection():

    conn = sqlite3.connect("sql/ipl_analysis.db")

    return conn
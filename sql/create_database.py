import pandas as pd
import sqlite3

# Load datasets
matches = pd.read_csv("data/processed/matches_cleaned.csv")
deliveries = pd.read_excel("data/raw/deliveries.xlsx")

# Create database
conn = sqlite3.connect("sql/ipl_analysis.db")

# Write tables
matches.to_sql("matches", conn, if_exists="replace", index=False)
deliveries.to_sql("deliveries", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("Database Created Successfully!")
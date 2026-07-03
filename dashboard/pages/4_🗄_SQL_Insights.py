import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

from styles import load_css
from sidebar import show_sidebar

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="SQL Insights",
    page_icon="🗄️",
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

st.title("🗄️ SQL Insights Dashboard")
st.caption("SQL Analysis performed on the IPL SQLite Database")

st.divider()

# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------

conn = sqlite3.connect("sql/ipl_analysis.db")

# ---------------------------------------------------
# QUERY 1 - TEAM WINS
# ---------------------------------------------------

query1 = """
SELECT winner,
COUNT(*) AS Wins
FROM matches
WHERE winner IS NOT NULL
GROUP BY winner
ORDER BY Wins DESC;
"""

team_wins = pd.read_sql(query1, conn)

st.subheader("🏆 Team Wins (SQL)")

fig = px.bar(
    team_wins,
    x="winner",
    y="Wins",
    text="Wins",
    color="Wins",
    color_continuous_scale="Viridis"
)

fig.update_layout(
    xaxis_title="Team",
    yaxis_title="Wins",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# QUERY 2 - PLAYER OF THE MATCH
# ---------------------------------------------------

query2 = """
SELECT player_of_match,
COUNT(*) AS Awards
FROM matches
WHERE player_of_match IS NOT NULL
GROUP BY player_of_match
ORDER BY Awards DESC
LIMIT 10;
"""

mvp = pd.read_sql(query2, conn)

st.subheader("⭐ Top Player of the Match Winners")

st.dataframe(
    mvp,
    use_container_width=True
)

# ---------------------------------------------------
# QUERY 3 - MATCHES PER SEASON
# ---------------------------------------------------

query3 = """
SELECT season,
COUNT(*) AS Matches
FROM matches
GROUP BY season
ORDER BY season;
"""

season = pd.read_sql(query3, conn)

fig2 = px.line(
    season,
    x="season",
    y="Matches",
    markers=True,
    title="Matches Played Per Season"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ---------------------------------------------------
# QUERY 4 - TOSS DECISIONS
# ---------------------------------------------------

query4 = """
SELECT toss_decision,
COUNT(*) AS Total
FROM matches
GROUP BY toss_decision;
"""

toss = pd.read_sql(query4, conn)

fig3 = px.pie(
    toss,
    names="toss_decision",
    values="Total",
    title="Toss Decision Distribution"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ---------------------------------------------------
# QUERY 5 - TOP VENUES
# ---------------------------------------------------

query5 = """
SELECT venue,
COUNT(*) AS Matches
FROM matches
GROUP BY venue
ORDER BY Matches DESC
LIMIT 10;
"""

venues = pd.read_sql(query5, conn)

fig4 = px.bar(
    venues,
    x="venue",
    y="Matches",
    text="Matches",
    color="Matches",
    color_continuous_scale="Blues"
)

fig4.update_layout(
    xaxis_tickangle=-45
)

st.subheader("🏟️ Top IPL Venues")

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ---------------------------------------------------
# CUSTOM SQL
# ---------------------------------------------------

st.divider()

st.subheader("💻 Run Your Own SQL Query")

user_query = st.text_area(
    "Write your SQL query",
    value="SELECT * FROM matches LIMIT 10;",
    height=150
)

if st.button("▶ Run Query"):

    try:
        result = pd.read_sql(user_query, conn)
        st.dataframe(
            result,
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Error: {e}")

conn.close()
import streamlit as st
import pandas as pd
import plotly.express as px

from styles import load_css
from sidebar import show_sidebar

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Player Analysis",
    page_icon="👤",
    layout="wide"
)

load_css()

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

matches = pd.read_csv("data/processed/matches_cleaned.csv")
deliveries = pd.read_excel("data/raw/deliveries.xlsx")

# Merge season into deliveries
deliveries = deliveries.merge(
    matches[["id", "season", "team1", "team2"]],
    left_on="match_id",
    right_on="id",
    how="left"
)

deliveries.drop(columns=["id"], inplace=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

selected_season, selected_team = show_sidebar(matches)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

filtered_matches = matches.copy()

if selected_season != "All Seasons":
    filtered_matches = filtered_matches[
        filtered_matches["season"].astype(str) == selected_season
    ]

filtered_deliveries = deliveries[
    deliveries["match_id"].isin(filtered_matches["id"])
]

# ---------------------------------------------------
# PLAYER LIST
# ---------------------------------------------------

if selected_team != "All Teams":

    team_matches = filtered_matches[
        (filtered_matches["team1"] == selected_team)
        | (filtered_matches["team2"] == selected_team)
    ]

    filtered_deliveries = filtered_deliveries[
        filtered_deliveries["match_id"].isin(team_matches["id"])
    ]

players = sorted(
    filtered_deliveries["batter"]
    .dropna()
    .unique()
)

selected_player = st.selectbox(
    "Select Player",
    players
)

# ---------------------------------------------------
# PLAYER DATA
# ---------------------------------------------------

batting = filtered_deliveries[
    filtered_deliveries["batter"] == selected_player
]

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

total_runs = batting["batsman_runs"].sum()
balls = len(batting)
innings = batting["match_id"].nunique()
fours = (batting["batsman_runs"] == 4).sum()
sixes = (batting["batsman_runs"] == 6).sum()

strike_rate = (
    (total_runs / balls) * 100
    if balls > 0
    else 0
)

st.title("👤 Player Analysis")
st.caption(f"Detailed batting statistics for **{selected_player}**")

st.divider()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Runs", total_runs)
c2.metric("Innings", innings)
c3.metric("Strike Rate", f"{strike_rate:.2f}")
c4.metric("Sixes", sixes)

st.metric("Fours", fours)

st.divider()

# ---------------------------------------------------
# RUNS PER SEASON
# ---------------------------------------------------

season_runs = (
    batting.groupby("season")["batsman_runs"]
    .sum()
    .reset_index()
)

fig = px.bar(
    season_runs,
    x="season",
    y="batsman_runs",
    title=f"{selected_player} - Runs Per Season",
    text="batsman_runs",
    color="batsman_runs",
    color_continuous_scale="Oranges"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# DISMISSAL TYPES
# ---------------------------------------------------

dismissals = (
    batting["dismissal_kind"]
    .fillna("Not Out")
    .value_counts()
    .reset_index()
)

dismissals.columns = [
    "Dismissal",
    "Count"
]

fig2 = px.pie(
    dismissals,
    names="Dismissal",
    values="Count",
    title="Dismissal Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ---------------------------------------------------
# MATCH-WISE RUNS
# ---------------------------------------------------

match_runs = (
    batting.groupby("match_id")["batsman_runs"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    match_runs,
    x="match_id",
    y="batsman_runs",
    markers=True,
    title="Runs Scored Match by Match"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ---------------------------------------------------
# BALL-BY-BALL DATA
# ---------------------------------------------------

with st.expander("View Ball-by-Ball Data"):

    st.dataframe(
        batting.reset_index(drop=True),
        use_container_width=True
    )
import streamlit as st
import pandas as pd
import plotly.express as px

from styles import load_css
from sidebar import show_sidebar

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Team Analysis",
    page_icon="📊",
    layout="wide"
)

load_css()

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

matches = pd.read_csv("data/processed/matches_cleaned.csv")

# Shared Sidebar
selected_season, selected_team = show_sidebar(matches)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

filtered_matches = matches.copy()

if selected_season != "All Seasons":
    filtered_matches = filtered_matches[
        filtered_matches["season"].astype(str) == selected_season
    ]

# Use sidebar team if selected, otherwise allow page selection
if selected_team != "All Teams":
    team = selected_team
else:
    team = st.selectbox(
        "Select Team",
        sorted(
            list(
                set(filtered_matches["team1"]).union(
                    set(filtered_matches["team2"])
                )
            )
        )
    )

team_matches = filtered_matches[
    (filtered_matches["team1"] == team) |
    (filtered_matches["team2"] == team)
]

wins = team_matches[team_matches["winner"] == team]

losses = len(team_matches) - len(wins)

win_percentage = (
    (len(wins) / len(team_matches)) * 100
    if len(team_matches) > 0
    else 0
)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("📊 Team Analysis")
st.caption(f"Detailed statistics for **{team}**")

st.divider()

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("Matches", len(team_matches))
c2.metric("Wins", len(wins))
c3.metric("Losses", losses)
c4.metric("Win %", f"{win_percentage:.2f}%")

st.divider()

# ---------------------------------------------------
# SEASON-WISE WINS
# ---------------------------------------------------

season_wins = (
    wins.groupby("season")
    .size()
    .reset_index(name="Wins")
)

fig = px.line(
    season_wins,
    x="season",
    y="Wins",
    markers=True,
    title=f"{team} Season-wise Wins"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# RECENT MATCHES
# ---------------------------------------------------

st.subheader("📅 Recent Matches")

st.dataframe(
    team_matches.sort_values(
        "date",
        ascending=False
    ).head(20),
    use_container_width=True
)
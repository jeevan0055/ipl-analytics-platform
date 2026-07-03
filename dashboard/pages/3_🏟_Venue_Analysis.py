import streamlit as st
import pandas as pd
import plotly.express as px

from styles import load_css
from sidebar import show_sidebar

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Venue Analysis",
    page_icon="🏟️",
    layout="wide"
)

load_css()

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

matches = pd.read_csv("data/processed/matches_cleaned.csv")

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

# ---------------------------------------------------
# VENUE SELECTION
# ---------------------------------------------------

venues = sorted(filtered_matches["venue"].dropna().unique())

selected_venue = st.selectbox(
    "Select Venue",
    venues
)

venue_matches = filtered_matches[
    filtered_matches["venue"] == selected_venue
]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🏟️ Venue Analysis")
st.caption(f"Detailed statistics for **{selected_venue}**")

st.divider()

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Matches Played",
    len(venue_matches)
)

c2.metric(
    "Unique Teams",
    len(
        set(venue_matches["team1"]).union(
            set(venue_matches["team2"])
        )
    )
)

average_target = (
    round(venue_matches["target_runs"].mean(), 1)
    if not venue_matches["target_runs"].isna().all()
    else 0
)

c3.metric(
    "Average Target",
    average_target
)

c4.metric(
    "Super Overs",
    (venue_matches["super_over"] == "Y").sum()
)

st.divider()

# ---------------------------------------------------
# WINNING TEAMS
# ---------------------------------------------------

winner_df = (
    venue_matches["winner"]
    .value_counts()
    .reset_index()
)

winner_df.columns = [
    "Team",
    "Wins"
]

fig = px.bar(
    winner_df,
    x="Team",
    y="Wins",
    color="Wins",
    text="Wins",
    title="Wins at this Venue",
    color_continuous_scale="Viridis"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# TOSS DECISION
# ---------------------------------------------------

toss_df = (
    venue_matches["toss_decision"]
    .value_counts()
    .reset_index()
)

toss_df.columns = [
    "Decision",
    "Matches"
]

fig2 = px.pie(
    toss_df,
    names="Decision",
    values="Matches",
    title="Toss Decision Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ---------------------------------------------------
# MATCHES PER SEASON
# ---------------------------------------------------

season_df = (
    venue_matches.groupby("season")
    .size()
    .reset_index(name="Matches")
)

fig3 = px.line(
    season_df,
    x="season",
    y="Matches",
    markers=True,
    title="Matches Hosted Per Season"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ---------------------------------------------------
# RECENT MATCHES
# ---------------------------------------------------

with st.expander("📅 Recent Matches"):

    st.dataframe(
        venue_matches.sort_values(
            "date",
            ascending=False
        ),
        use_container_width=True
    )
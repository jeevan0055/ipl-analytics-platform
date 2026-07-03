import streamlit as st
from PIL import Image

from styles import load_css
from sidebar import show_sidebar
from utils import load_data
from charts import (
    matches_per_season,
    team_wins,
    top_venues,
    orange_cap,
    purple_cap,
)

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="IPL Analytics Platform",
    page_icon="🏏",
    layout="wide",
)

load_css()

banner = Image.open("dashboard/assets/banner1.jpeg")
st.image(banner, use_container_width=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

matches, deliveries = load_data()

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

if selected_team != "All Teams":
    filtered_matches = filtered_matches[
        (filtered_matches["team1"] == selected_team)
        | (filtered_matches["team2"] == selected_team)
    ]

filtered_deliveries = deliveries[
    deliveries["match_id"].isin(filtered_matches["id"])
]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🏏 IPL Analytics Platform")
st.caption("Interactive Dashboard | Seasons 2008–2024")
st.divider()

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("Matches", len(filtered_matches))

c2.metric(
    "Teams",
    len(set(filtered_matches["team1"]).union(set(filtered_matches["team2"]))),
)

c3.metric(
    "Players",
    filtered_deliveries["batter"].nunique(),
)

c4.metric(
    "Deliveries",
    f"{len(filtered_deliveries):,}",
)

st.divider()

# ---------------------------------------------------
# CHARTS
# ---------------------------------------------------

left, right = st.columns(2)

with left:
    st.plotly_chart(
        matches_per_season(filtered_matches),
        use_container_width=True,
    )

with right:
    st.plotly_chart(
        team_wins(filtered_matches),
        use_container_width=True,
    )

left, right = st.columns(2)

with left:
    st.plotly_chart(
        orange_cap(filtered_deliveries),
        use_container_width=True,
    )

with right:
    st.plotly_chart(
        purple_cap(filtered_deliveries),
        use_container_width=True,
    )

st.plotly_chart(
    top_venues(filtered_matches),
    use_container_width=True,
)

# ---------------------------------------------------
# QUICK INSIGHTS
# ---------------------------------------------------

st.subheader("📌 Quick Insights")

best_team = (
    filtered_matches["winner"].mode().iloc[0]
    if not filtered_matches.empty
    else "N/A"
)

best_venue = (
    filtered_matches["venue"].mode().iloc[0]
    if not filtered_matches.empty
    else "N/A"
)

st.info(
    f"""
🏆 Most Successful Team: **{best_team}**

🏟 Most Frequent Venue: **{best_venue}**

📅 Seasons Selected: **{selected_season}**

👥 Team Selected: **{selected_team}**
"""
)

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------

with st.expander("View Filtered Match Data"):
    st.dataframe(filtered_matches)

# ---------------------------------------------------
# DOWNLOAD
# ---------------------------------------------------

csv = filtered_matches.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    "ipl_filtered_matches.csv",
    "text/csv",
)
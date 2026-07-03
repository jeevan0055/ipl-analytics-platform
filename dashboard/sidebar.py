import streamlit as st
import pandas as pd
from PIL import Image

def show_sidebar(matches):

    with st.sidebar:
        # Logo
        logo = Image.open("dashboard/assets/logo.png")
        st.image(logo, width=180)

        st.markdown("## 🏏 IPL Analytics Platform")
        st.markdown("---")

        # Season Filter
        seasons = sorted(matches["season"].unique())

        selected_season = st.selectbox(
            "Select Season",
            ["All Seasons"] + list(seasons)
        )

        # Team Filter
        teams = sorted(
            set(matches["team1"]).union(set(matches["team2"]))
        )

        selected_team = st.selectbox(
            "Select Team",
            ["All Teams"] + teams
        )

    return selected_season, selected_team
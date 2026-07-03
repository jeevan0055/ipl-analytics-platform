import plotly.express as px


# ---------------------------------------------------
# Matches Per Season
# ---------------------------------------------------

def matches_per_season(matches):

    season_data = (
        matches
        .groupby("season")
        .size()
        .reset_index(name="Matches")
    )

    fig = px.bar(
        season_data,
        x="season",
        y="Matches",
        title="Matches Played Per Season",
        text="Matches",
        color="Matches",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        xaxis_title="Season",
        yaxis_title="Matches",
        template="plotly_white"
    )

    return fig


# ---------------------------------------------------
# Team Wins
# ---------------------------------------------------

def team_wins(matches):

    wins = (
        matches["winner"]
        .value_counts()
        .reset_index()
    )

    wins.columns = ["Team", "Wins"]

    fig = px.bar(
        wins,
        x="Team",
        y="Wins",
        text="Wins",
        color="Wins",
        color_continuous_scale="Viridis",
        title="Total Wins by Team"
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        template="plotly_white"
    )

    return fig


# ---------------------------------------------------
# Top Venues
# ---------------------------------------------------

def top_venues(matches):

    venues = (
        matches["venue"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    venues.columns = ["Venue", "Matches"]

    fig = px.bar(
        venues,
        x="Venue",
        y="Matches",
        text="Matches",
        color="Matches",
        color_continuous_scale="Teal",
        title="Top 10 IPL Venues"
    )

    fig.update_layout(
        xaxis_tickangle=-35,
        template="plotly_white"
    )

    return fig


# ---------------------------------------------------
# Orange Cap
# ---------------------------------------------------

def orange_cap(deliveries):

    runs = (
        deliveries.groupby("batter")["batsman_runs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        runs,
        x="batter",
        y="batsman_runs",
        text="batsman_runs",
        color="batsman_runs",
        color_continuous_scale="Oranges",
        title="Top 10 Run Scorers"
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        xaxis_title="Player",
        yaxis_title="Runs",
        template="plotly_white"
    )

    return fig


# ---------------------------------------------------
# Purple Cap
# ---------------------------------------------------

def purple_cap(deliveries):

    wickets = (
        deliveries[
            deliveries["is_wicket"] == 1
        ]
        .groupby("bowler")
        .size()
        .sort_values(ascending=False)
        .head(10)
        .reset_index(name="Wickets")
    )

    fig = px.bar(
        wickets,
        x="bowler",
        y="Wickets",
        text="Wickets",
        color="Wickets",
        color_continuous_scale="Purples",
        title="Top 10 Wicket Takers"
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        template="plotly_white"
    )

    return fig
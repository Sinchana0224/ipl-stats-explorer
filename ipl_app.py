# ipl_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import analysis

st.set_page_config(page_title="IPL Stats Explorer", layout="wide")

st.markdown("""
    <style>
    h1, h2 { color: #1DB954; }
    .reportview-container .main .block-container{ padding-top: 1rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🏏 IPL Match Stats Explorer")

# --- Load Data ---
matches, deliveries = analysis.load_data()

# --- Sidebar Filters ---
st.sidebar.header("Filters")

seasons = sorted(matches['season'].unique())
selected_season = st.sidebar.selectbox("Select Season", seasons)
matches = matches[matches['season'] == selected_season]

teams = sorted(matches['team1'].unique())
selected_teams = st.sidebar.multiselect("Select Team(s)", teams, default=teams)
matches = matches[
    matches['team1'].isin(selected_teams) |
    matches['team2'].isin(selected_teams)
]

# --- Main View Option ---
st.sidebar.header("Choose View")
option = st.sidebar.radio("Stats Section", 
    ["Team Win Percentage", "Top Run Scorers", "Top Wicket Takers", "Toss Impact"]
)

# --- Section Rendering ---
if option == "Team Win Percentage":
    st.subheader(f"📊 Win % by Team ({selected_season})")
    win_counts, win_percent = analysis.get_team_win_stats(matches)
    fig = px.bar(
        win_percent.sort_values(), 
        orientation='h', 
        title=f"Win % - {selected_season}", 
        labels={'value': 'Win %', 'index': 'Team'},
        color=win_percent.sort_values(),
        color_continuous_scale='Greens'
    )
    st.plotly_chart(fig, use_container_width=True)

elif option == "Top Run Scorers":
    st.subheader("🏏 Top Run Scorers")
    top_scorers = analysis.get_top_scorers(deliveries)
    st.bar_chart(top_scorers)

elif option == "Top Wicket Takers":
    st.subheader("🎯 Top Wicket Takers")
    top_bowlers = analysis.get_top_wicket_takers(deliveries)
    st.bar_chart(top_bowlers)

elif option == "Toss Impact":
    st.subheader("🧠 Does Toss Matter?")
    toss_win_rate = analysis.toss_win_analysis(matches)
    st.metric(label="Toss Winner Also Won", value=f"{toss_win_rate:.2f}%")

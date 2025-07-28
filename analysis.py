# analysis.py

import pandas as pd

def load_data():
    matches = pd.read_csv("data/matches.csv")
    deliveries = pd.read_csv("data/deliveries.csv")
    
    # Optional: Normalize column names to lowercase
    matches.columns = [col.lower() for col in matches.columns]
    deliveries.columns = [col.lower() for col in deliveries.columns]
    
    return matches, deliveries

def get_team_win_stats(matches):
    win_counts = matches['winner'].value_counts()
    total_matches = pd.concat([matches['team1'], matches['team2']]).value_counts()
    win_percent = (win_counts / total_matches) * 100
    return win_counts, win_percent.fillna(0)

def get_top_scorers(deliveries, top_n=10):
    return (
        deliveries.groupby('batter')['batsman_runs']
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
    )

def get_top_wicket_takers(deliveries, top_n=10):
    wickets = deliveries[deliveries['dismissal_kind'].notnull()]
    return wickets['bowler'].value_counts().head(top_n)

def toss_win_analysis(matches):
    toss_win = matches[matches['toss_winner'] == matches['winner']]
    toss_win_rate = (len(toss_win) / len(matches)) * 100
    return toss_win_rate

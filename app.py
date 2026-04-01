import streamlit as st
import pandas as pd

st.set_page_config(page_title="NBA Player Comparison", layout="wide")

df = pd.read_csv("nba_player_stats.csv")

st.title("🏀 NBA Player Analytics Dashboard")

players = df["Player"].unique()

col1, col2 = st.columns(2)

with col1:
    player1 = st.selectbox("Select Player 1", players)

with col2:
    player2 = st.selectbox("Select Player 2", players)

df1 = df[df["Player"] == player1]
df2 = df[df["Player"] == player2]

season = st.selectbox("Select Season", sorted(df["Season"].unique()))

row1 = df1[df1["Season"] == season]
row2 = df2[df2["Season"] == season]

if not row1.empty and not row2.empty:
    row1 = row1.iloc[0]
    row2 = row2.iloc[0]

    st.subheader(f"{player1} vs {player2} ({season})")

    st.write("PPG:", row1["PPG"], "|", row2["PPG"])
    st.write("AST:", row1["AST"], "|", row2["AST"])
    st.write("REB:", row1["REB"], "|", row2["REB"])

else:
    st.warning("One player didn't play this season")

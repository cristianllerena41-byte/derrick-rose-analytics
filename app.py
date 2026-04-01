iimport streamlit as st
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="NBA Player Comparison", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.main {
    background: linear-gradient(to bottom, #0b0f1a, #111);
}
h1 {
    color: #00c6ff;
}
.stat-box {
    background: linear-gradient(145deg, #1c1f26, #111);
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 0 10px rgba(0,198,255,0.2);
}
</style>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
df = pd.read_csv("nba_player_stats.csv")

# ---------- TITLE ----------
st.title("🏀 NBA Player Analytics Dashboard")

# ---------- PLAYER SELECT ----------
players = df["Player"].unique()

col1, col2 = st.columns(2)

with col1:
    player1 = st.selectbox("Select Player 1", players)

with col2:
    player2 = st.selectbox("Select Player 2", players)

# ---------- FILTER ----------
df1 = df[df["Player"] == player1]
df2 = df[df["Player"] == player2]

# ---------- SEASON SELECT ----------
season = st.selectbox("Select Season", sorted(df["Season"].unique()))

row1 = df1[df1["Season"] == season]
row2 = df2[df2["Season"] == season]

st.markdown("---")

# ---------- COMPARISON ----------
if not row1.empty and not row2.empty:

    row1 = row1.iloc[0]
    row2 = row2.iloc[0]

    st.subheader(f"🔥 {player1} vs {player2} ({season})")

    stats = ["PPG", "AST", "REB", "FG%", "TS%", "USG"]

    cols = st.columns(len(stats))

    for i, stat in enumerate(stats):
        v1 = float(row1[stat])
        v2 = float(row2[stat])

        diff = round(v1 - v2, 2)

        color = "#00ffcc" if diff > 0 else "#ff4d4d"

        cols[i].markdown(f"""
        <div class="stat-box">
            <h4>{stat}</h4>
            <p>{player1}: {v1}</p>
            <p>{player2}: {v2}</p>
            <p style='color:{color}; font-weight:bold;'>Diff: {diff}</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------- WINNER ----------
    score1 = row1["PPG"] + row1["AST"] + row1["REB"]
    score2 = row2["PPG"] + row2["AST"] + row2["REB"]

    if score1 > score2:
        st.success(f"🏆 {player1} had the better season")
    elif score2 > score1:
        st.success(f"🏆 {player2} had the better season")
    else:
        st.info("It's a tie")

    # ---------- EXTRA INFO ----------
    st.markdown("### 📌 Season Info")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"""
        **{player1}**
        - Team: {row1["Team"]}
        - FG%: {row1["FG%"]}
        - TS%: {row1["TS%"]}
        - Usage: {row1["USG"]}
        - Notes: {row1["Notes"]}
        """)

    with c2:
        st.markdown(f"""
        **{player2}**
        - Team: {row2["Team"]}
        - FG%: {row2["FG%"]}
        - TS%: {row2["TS%"]}
        - Usage: {row2["USG"]}
        - Notes: {row2["Notes"]}
        """)

else:
    st.warning("⚠️ One player didn't play this season")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("🚀 Built by Cristian Llerena | Sports Analytics Project")

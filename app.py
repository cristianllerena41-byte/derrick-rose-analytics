import streamlit as st
import pandas as pd

# ---------- PAGE ----------
st.set_page_config(page_title="NBA Analytics", layout="wide")

# ---------- ESPN STYLE ----------
st.markdown("""
<style>

/* Background */
.main {
    background: linear-gradient(to bottom, #0a0f1f, #05070d);
}

/* Title */
h1 {
    color: #ff0033;
    text-align: center;
    font-size: 42px;
}

/* Section headers */
h3 {
    color: #00c6ff;
}

/* Cards */
.card {
    background: linear-gradient(145deg, #111, #1a1a1a);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 0 15px rgba(255,0,51,0.3);
    border-top: 4px solid #ff0033;
}

/* Winner / loser colors */
.win {
    color: #00ffcc;
    font-weight: bold;
    font-size: 18px;
}
.lose {
    color: #ff4d4d;
    font-size: 16px;
}

/* Dropdown styling */
div[data-baseweb="select"] {
    border: 2px solid #ff0033;
    border-radius: 8px;
}

/* Table */
[data-testid="stDataFrame"] {
    border: 2px solid #00c6ff;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
df = pd.read_csv("nba_player_stats.csv")

st.title("🏀 NBA Player Analytics Dashboard")

# ---------- SELECT ----------
players = df["Player"].unique()

c1, c2 = st.columns(2)

with c1:
    p1 = st.selectbox("🔥 Player 1", players)

with c2:
    p2 = st.selectbox("🔥 Player 2", players)

season = st.selectbox("📅 Select Season", sorted(df["Season"].unique()))

# ---------- FILTER ----------
r1 = df[(df["Player"] == p1) & (df["Season"] == season)]
r2 = df[(df["Player"] == p2) & (df["Season"] == season)]

st.markdown("---")

if not r1.empty and not r2.empty:

    r1 = r1.iloc[0]
    r2 = r2.iloc[0]

    st.subheader(f"⚔️ {p1} vs {p2} ({season})")

    # ---------- MAIN STATS ----------
    st.markdown("### 🏆 Key Stats")

    main_stats = ["PPG", "AST", "REB"]
    cols = st.columns(3)

    for i, stat in enumerate(main_stats):
        v1 = float(r1[stat])
        v2 = float(r2[stat])

        if v1 > v2:
            c1_color, c2_color = "win", "lose"
        elif v2 > v1:
            c1_color, c2_color = "lose", "win"
        else:
            c1_color = c2_color = ""

        cols[i].markdown(f"""
        <div class="card">
            <h3>{stat}</h3>
            <p class="{c1_color}">{p1}: {v1}</p>
            <p class="{c2_color}">{p2}: {v2}</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------- ADVANCED ----------
    st.markdown("### 📊 Advanced Metrics")

    adv_stats = ["FG%", "TS%", "USG"]
    cols2 = st.columns(3)

    for i, stat in enumerate(adv_stats):
        v1 = float(r1[stat])
        v2 = float(r2[stat])

        if v1 > v2:
            c1_color, c2_color = "win", "lose"
        elif v2 > v1:
            c1_color, c2_color = "lose", "win"
        else:
            c1_color = c2_color = ""

        cols2[i].markdown(f"""
        <div class="card" style="border-top:4px solid #00c6ff;">
            <h4>{stat}</h4>
            <p class="{c1_color}">{p1}: {v1}</p>
            <p class="{c2_color}">{p2}: {v2}</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------- WINNER ----------
    score1 = r1["PPG"] + r1["AST"] + r1["REB"]
    score2 = r2["PPG"] + r2["AST"] + r2["REB"]

    if score1 > score2:
        st.success(f"🏆 {p1} DOMINATES THIS SEASON")
    elif score2 > score1:
        st.success(f"🏆 {p2} DOMINATES THIS SEASON")
    else:
        st.info("🤝 EVEN MATCHUP")

    # ---------- FULL TABLE ----------
    st.markdown("### 📋 Full Breakdown")

    compare_df = pd.DataFrame({
        "Stat": ["PPG", "AST", "REB", "FG%", "TS%", "USG"],
        p1: [r1["PPG"], r1["AST"], r1["REB"], r1["FG%"], r1["TS%"], r1["USG"]],
        p2: [r2["PPG"], r2["AST"], r2["REB"], r2["FG%"], r2["TS%"], r2["USG"]],
    })

    st.dataframe(compare_df, use_container_width=True)

    # ---------- INFO ----------
    st.markdown("### 📌 Season Info")

    i1, i2 = st.columns(2)

    with i1:
        st.markdown(f"**{p1}**")
        st.write(f"Team: {r1['Team']}")
        st.write(f"Notes: {r1['Notes']}")

    with i2:
        st.markdown(f"**{p2}**")
        st.write(f"Team: {r2['Team']}")
        st.write(f"Notes: {r2['Notes']}")

else:
    st.warning("⚠️ One player didn’t play this season")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("🚀 Built by Cristian Llerena | ESPN Style Dashboard")

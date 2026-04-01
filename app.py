import streamlit as st
import pandas as pd

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Derrick Rose Analytics", layout="wide")

# ---- 🔥 STYLE (ESPN LOOK) ----
st.markdown("""
<style>
.main {
    background: linear-gradient(to bottom, #0E1117, #05070c);
}

h1 {
    color: #00BFFF;
}

/* STAT CARDS */
.stMetric {
    background: linear-gradient(145deg, #1c1f26, #111);
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #00BFFF33;
    text-align: center;
}

/* COLOR ACCENTS */
div[data-testid="metric-container"]:nth-child(1) {
    border-left: 5px solid #00BFFF;
}
div[data-testid="metric-container"]:nth-child(2) {
    border-left: 5px solid #00FFAA;
}
div[data-testid="metric-container"]:nth-child(3) {
    border-left: 5px solid #FF4B4B;
}
div[data-testid="metric-container"]:nth-child(4) {
    border-left: 5px solid #FFD700;
}
</style>
""", unsafe_allow_html=True)

# ---- LOAD DATA ----
df = pd.read_csv("derrick_rose_career.csv")

# ---- TITLE ----
st.title("🏀 Derrick Rose Player Dashboard")

# ---- TEAM FILTER ----
teams = st.sidebar.multiselect(
    "Teams",
    df["Team"].unique(),
    default=df["Team"].unique()
)

df_filtered = df[df["Team"].isin(teams)]

# ---- SELECT SEASON ----
season = st.selectbox("Select Season", df_filtered["Season"])
row = df_filtered[df_filtered["Season"] == season].iloc[0]

st.markdown("---")

# ---- 🔥 MAIN STATS ----
st.markdown(f"## 🔥 {season} Season Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("🏀 PPG", row["PPG"])
c2.metric("🎯 AST", row["AST"])
c3.metric("💪 REB", row["REB"])
c4.metric("📊 FG%", row["FG%"])

# ---- ADVANCED STATS ----
c5, c6, c7, c8 = st.columns(4)

c5.metric("⚡ TS%", row["TS%"])
c6.metric("🔥 USG%", row["USG"])
c7.metric("📈 Impact", round(row["PPG"] + row["AST"] + row["REB"],1))
c8.metric("🧠 Efficiency", round(row["TS%"] * row["USG"] / 10,1))

st.markdown("---")

# ---- PLAYER INFO CARD ----
st.markdown(f"""
<div style="
background: linear-gradient(145deg,#1c1f26,#111);
padding:20px;
border-radius:12px;
border-left:5px solid #00BFFF;
">
<h3 style="color:#00BFFF;">📌 Season Info</h3>
<b>Team:</b> {row['Team']}<br>
<b>Season:</b> {season}<br>
<b>FG%:</b> {row['FG%']}<br>
<b>TS%:</b> {row['TS%']}<br>
<b>USG%:</b> {row['USG']}<br>
<b>Notes:</b> {row['Notes']}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---- MINI VISUAL BAR (CLEAN + COLORFUL) ----
st.subheader("📊 Stat Comparison")

stats = ["PPG", "AST", "REB", "TS%", "USG"]
values = [
    row["PPG"],
    row["AST"],
    row["REB"],
    row["TS%"],
    row["USG"]
]

colors = ["#00BFFF", "#00FFAA", "#FF4B4B", "#FFD700", "#9B59B6"]

bar_cols = st.columns(len(stats))

for i in range(len(stats)):
    bar_cols[i].markdown(f"""
    <div style="text-align:center">
        <div style="font-size:20px;color:{colors[i]}">{stats[i]}</div>
        <div style="font-size:28px;color:white;font-weight:bold">{values[i]}</div>
        <div style="height:8px;background:{colors[i]};border-radius:5px;margin-top:8px"></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---- TABLE (ONLY THAT SEASON) ----
st.dataframe(df_filtered[df_filtered["Season"] == season], use_container_width=True)

# ---- FOOTER ----
st.caption("🚀 Built by Cristian Llerena | Sports Analytics Project")

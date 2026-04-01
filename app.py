import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Derrick Rose Analytics", layout="wide")

# ---- STYLE ----
st.markdown("""
<style>
.main {
    background: linear-gradient(to bottom, #0E1117, #05070c);
}
h1 {color: #00BFFF;}
.stMetric {
    background: linear-gradient(145deg, #1c1f26, #111);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #00BFFF33;
}
</style>
""", unsafe_allow_html=True)

# ---- LOAD ----
df = pd.read_csv("derrick_rose_career.csv")

# ---- TITLE ----
st.title("🏀 Derrick Rose Player Dashboard")

# ---- SELECT SEASON ----
season = st.selectbox("Select Season", df["Season"])
row = df[df["Season"] == season].iloc[0]

st.markdown("---")

# ---- MAIN STATS (BIG CARDS) ----
st.subheader(f"🔥 {season} Season")

c1, c2, c3, c4 = st.columns(4)

c1.metric("PPG", row["PPG"])
c2.metric("AST", row["AST"])
c3.metric("REB", row["REB"])
c4.metric("FG%", row["FG%"])

# ---- ADVANCED STATS ----
c5, c6, c7 = st.columns(3)

c5.metric("TS%", row["TS%"])
c6.metric("USG%", row["USG"])
c7.metric("Efficiency Score", round(row["TS%"] * row["USG"] / 10, 1))

# ---- PLAYER CARD ----
st.markdown(f"""
<div style="background:linear-gradient(145deg,#1c1f26,#111);
padding:20px;border-radius:12px">
<h3 style="color:#00BFFF;">Season Info</h3>
<b>Team:</b> {row['Team']}<br>
<b>Notes:</b> {row['Notes']}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---- RADAR CHART (🔥 THIS IS THE COOL PART) ----
st.subheader("🎯 Performance Breakdown")

categories = ["PPG", "AST", "REB", "FG%", "TS%", "USG"]

values = [
    row["PPG"],
    row["AST"],
    row["REB"],
    row["FG%"],
    row["TS%"],
    row["USG"]
]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    line=dict(color="#00BFFF")
))

fig.update_layout(
    polar=dict(
        bgcolor="#1c1f26",
        radialaxis=dict(visible=True, color="white")
    ),
    paper_bgcolor="#0E1117",
    font=dict(color="white")
)

st.plotly_chart(fig, use_container_width=True)

# ---- OPTIONAL TABLE ----
st.markdown("---")
st.dataframe(df[df["Season"] == season])

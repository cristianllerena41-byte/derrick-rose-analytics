import streamlit as st
import pandas as pd
import plotly.express as px

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Derrick Rose Analytics", layout="wide")

# ---- 🔥 ESPN STYLE ----
st.markdown("""
<style>
.main {
    background: linear-gradient(to bottom, #0E1117, #05070c);
}
h1 {
    color: #00BFFF;
}
h2, h3 {
    color: white;
}
.stMetric {
    background: linear-gradient(145deg, #1c1f26, #111);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #00BFFF33;
}
</style>
""", unsafe_allow_html=True)

# ---- LOAD DATA ----
df = pd.read_csv("derrick_rose_career.csv")

# ---- TITLE ----
st.title("🏀 Derrick Rose Advanced Analytics Dashboard")

# ---- FILTER ----
teams = st.sidebar.multiselect(
    "Teams",
    df["Team"].unique(),
    default=df["Team"].unique()
)

df_filtered = df[df["Team"].isin(teams)]

# ---- TOP METRICS ----
st.subheader("📊 Career Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("PPG", round(df_filtered["PPG"].mean(),1))
c2.metric("AST", round(df_filtered["AST"].mean(),1))
c3.metric("TS%", round(df_filtered["TS%"].mean(),1))
c4.metric("USG%", round(df_filtered["USG"].mean(),1))

st.markdown("---")

# ---- SEASON SELECTOR ----
st.subheader("🎯 Season Breakdown")

season = st.selectbox("Pick a season", df["Season"])
row = df[df["Season"] == season].iloc[0]

a,b,c,d = st.columns(4)

a.metric("PPG", row["PPG"])
b.metric("AST", row["AST"])
c.metric("TS%", row["TS%"])
d.metric("USG%", row["USG"])

st.markdown(f"""
<div style="background: linear-gradient(145deg,#1c1f26,#111);padding:15px;border-radius:10px">
<b>Team:</b> {row['Team']}<br>
<b>FG%:</b> {row['FG%']}<br>
<b>Notes:</b> {row['Notes']}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---- SCORING TREND (🔥 GLOW + COLOR) ----
st.subheader("📈 Scoring Trend")

fig = px.line(
    df_filtered,
    x="Season",
    y="PPG",
    markers=True,
    text="PPG"
)

fig.update_xaxes(type='category')

# BASE LINE (faded)
fig.update_traces(
    line=dict(color="#444", width=2),
    marker=dict(size=8, color="#444"),
    textposition="top center"
)

# 🔥 HIGHLIGHT SELECTED
selected_row = df[df["Season"] == season]

fig.add_scatter(
    x=selected_row["Season"],
    y=selected_row["PPG"],
    mode="markers+text",
    marker=dict(size=18, color="#00BFFF", line=dict(width=3, color="white")),
    text=selected_row["PPG"],
    textposition="top center",
    name="Selected"
)

fig.update_layout(
    plot_bgcolor="#1c1f26",
    paper_bgcolor="#0E1117",
    font=dict(color="white"),
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# ---- TS% GRAPH (🔥 COLOR POP) ----
st.subheader("🎯 Efficiency (TS%)")

colors = [
    "#00FFAA" if s == season else "#222"
    for s in df_filtered["Season"]
]

fig2 = px.bar(
    df_filtered,
    x="Season",
    y="TS%",
    text="TS%",
    color=colors,
    color_discrete_map="identity"
)

fig2.update_xaxes(type='category')

fig2.update_traces(
    textposition="outside"
)

fig2.update_layout(
    plot_bgcolor="#1c1f26",
    paper_bgcolor="#0E1117",
    font=dict(color="white")
)

st.plotly_chart(fig2, use_container_width=True)

# ---- INSIGHTS ----
col1, col2 = st.columns(2)

with col1:
    mvp = df[df["Notes"] == "MVP"]
    st.success(f"MVP: {mvp['Season'].values[0]} ({mvp['PPG'].values[0]} PPG)")

with col2:
    best = df.loc[df["PPG"].idxmax()]
    st.info(f"Best Season: {best['Season']} ({best['PPG']} PPG)")

# ---- TABLE ----
st.markdown("---")
st.dataframe(df_filtered, use_container_width=True)

# ---- FOOTER ----
st.caption("🚀 Built by Cristian Llerena | Sports Analytics Project")

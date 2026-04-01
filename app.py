import streamlit as st
import pandas as pd
import plotly.express as px

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Derrick Rose Analytics", layout="wide")

# ---- STYLE ----
st.markdown("""
<style>
.main {background-color: #0E1117;}
h1, h2, h3 {color: white;}
.stMetric {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 10px;
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

# ---- SEASON EXPLORER ----
st.subheader("🎯 Season Breakdown")

season = st.selectbox("Pick a season", df["Season"])
row = df[df["Season"] == season].iloc[0]

a,b,c,d = st.columns(4)

a.metric("PPG", row["PPG"])
b.metric("AST", row["AST"])
c.metric("TS%", row["TS%"])
d.metric("USG%", row["USG"])

st.markdown(f"""
**Team:** {row['Team']}  
**FG%:** {row['FG%']}  
**Notes:** {row['Notes']}
""")

st.markdown("---")

# ---- SCORING TREND (FIXED + CLEAN) ----
st.subheader("📈 Scoring Trend")

fig = px.line(
    df_filtered,
    x="Season",
    y="PPG",
    markers=True,
    text="PPG"
)

# FIX AXIS (VERY IMPORTANT)
fig.update_xaxes(type='category')

# STYLE
fig.update_traces(
    line=dict(color="#00BFFF", width=4),
    marker=dict(size=10, color="#00BFFF"),
    textposition="top center"
)

fig.update_layout(
    plot_bgcolor="#1c1f26",
    paper_bgcolor="#0E1117",
    font=dict(color="white"),
    title="Points Per Game by Season",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# ---- EFFICIENCY CHART ----
st.subheader("🎯 Efficiency (TS%)")

fig2 = px.bar(
    df_filtered,
    x="Season",
    y="TS%",
    text="TS%"
)

# FIX AXIS
fig2.update_xaxes(type='category')

# STYLE
fig2.update_traces(
    marker_color="#00FFAA",
    textposition="outside"
)

fig2.update_layout(
    plot_bgcolor="#1c1f26",
    paper_bgcolor="#0E1117",
    font=dict(color="white"),
    title="True Shooting % by Season"
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

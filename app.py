import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Derrick Rose Analytics", layout="wide")

# Title
st.title("🏀 Derrick Rose Career Analytics Dashboard")

# Load data
df = pd.read_csv("derrick_rose_career.csv")

# Sidebar filters
st.sidebar.header("Filters")

teams = st.sidebar.multiselect(
    "Select Team(s):",
    options=df["Team"].unique(),
    default=df["Team"].unique()
)

df_filtered = df[df["Team"].isin(teams)]

# Layout
col1, col2 = st.columns(2)

# Metrics
with col1:
    st.subheader("📊 Career Averages")
    st.metric("PPG", round(df_filtered["PPG"].mean(), 1))
    st.metric("AST", round(df_filtered["AST"].mean(), 1))
    st.metric("REB", round(df_filtered["REB"].mean(), 1))

# Table
with col2:
    st.subheader("📋 Data Table")
    st.dataframe(df_filtered, use_container_width=True)

# Chart
st.subheader("📈 Points Per Game Over Time")

fig, ax = plt.subplots()
ax.plot(df_filtered["Season"], df_filtered["PPG"], marker='o')
plt.xticks(rotation=45)
plt.xlabel("Season")
plt.ylabel("PPG")
plt.title("Derrick Rose Scoring Trend")

st.pyplot(fig)

# MVP
st.subheader("🏆 MVP Season")
mvp = df[df["Notes"] == "MVP"]
st.success(f"{mvp['Season'].values[0]} with {mvp['PPG'].values[0]} PPG")

# Best season
st.subheader("🔥 Best Scoring Season")
best = df.loc[df["PPG"].idxmax()]
st.info(f"{best['Season']} - {best['PPG']} PPG")

# Footer
st.markdown("---")
st.caption("Data visualization project by Cristian Llerena")

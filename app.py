import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Derrick Rose Dashboard", layout="wide")
st.title("Derrick Rose — Career Dashboard")

PATH = "data/derrick_rose_career.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    # SeasonStart: "2010-11" -> 2010
    df["SeasonStart"] = pd.to_numeric(df["Season"].astype(str).str[:4], errors="coerce")

    # Turn stats into numbers (if they exist)
    for col in ["PTS", "AST", "TRB", "MP", "FG%", "3P%", "FT%"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["SeasonStart"]).sort_values("SeasonStart")
    return df

df = load_data(PATH)

# ---- Sidebar filters ----
st.sidebar.header("Filters")

metric_list = [c for c in ["PTS", "AST", "TRB", "MP", "FG%", "3P%", "FT%"] if c in df.columns]
metric = st.sidebar.selectbox("Choose a Stat", metric_list)

team_list = ["All"] + sorted(df["Tm"].dropna().unique().tolist()) if "Tm" in df.columns else ["All"]
team = st.sidebar.selectbox("Team", team_list)

min_year = int(df["SeasonStart"].min())
max_year = int(df["SeasonStart"].max())
years = st.sidebar.slider("Year Range", min_year, max_year, (min_year, max_year))

# Apply filters
filtered = df[(df["SeasonStart"] >= years[0]) & (df["SeasonStart"] <= years[1])]
if team != "All" and "Tm" in filtered.columns:
    filtered = filtered[filtered["Tm"] == team]

# ---- Charts ----
st.subheader(f"{metric} Over Time")
fig1 = px.line(filtered, x="SeasonStart", y=metric, markers=True, hover_data=["Season"] + (["Tm"] if "Tm" in filtered.columns else []))
st.plotly_chart(fig1, use_container_width=True)

if "Tm" in df.columns:
    st.subheader(f"Average {metric} by Team")
    team_avg = filtered.groupby("Tm", as_index=False)[metric].mean().sort_values(metric, ascending=False)
    fig2 = px.bar(team_avg, x="Tm", y=metric)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Table")
st.dataframe(filtered, use_container_width=True)


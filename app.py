import pandas as pd
import streamlit as st

st.set_page_config(page_title="Derrick Rose Dashboard", layout="wide")
st.title("Derrick Rose — Career Dashboard")

PATH = "data/derrick_rose_career.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]  # clean column names
    return df

df = load_data(PATH)

st.subheader("Data Preview")
st.dataframe(df, use_container_width=True)
st.write("Columns:", list(df.columns))

import pandas as pd
import streamlit as st

@st.cache_data(ttl=60) # ttl sets the tick time/ how often it refreshes the cache, in seconds. 60 seconds = 1 minute. If complaints, lower
def load_sheet(sheet_id: str, gid: str) -> pd.DataFrame:
    """
    Loads in a Google Sheet as a DataFrame and refreshes every 60 seconds.
    """
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)
    df = df.dropna(how="all")
    df = df.fillna("")
    return df

import streamlit as st
import pandas as pd

st.title("📞 Vendor Contacts")
st.caption("Search for vendor representatives and contact information.")

SHEET_ID = "18dn2ojjVdkF8QU1qTURwm3GmqOR2-eYvIn2IjGpUg4k"
GID = "980561560"

@st.cache_data(ttl=300)
def load_contacts():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"
    df = pd.read_csv(url)
    return df.dropna(how="all")

df = load_contacts()

search = st.text_input(
    "🔍 Search",
    placeholder="Vendor, rep, phone, email..."
)

if search:
    mask = df.astype(str).apply(
        lambda row: row.str.contains(search, case=False, na=False).any(),
        axis=1
    )
    filtered = df[mask]
else:
    filtered = df

st.write(f"Showing **{len(filtered)}** result(s)")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)
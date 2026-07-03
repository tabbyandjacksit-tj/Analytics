import streamlit as st
import pandas as pd

# ---------------------------------------
# Page Header
# ---------------------------------------

st.title("📞 Vendor Contacts")
st.caption("Search vendor representatives, emails, phone numbers, and brand policies.")

# ---------------------------------------
# Google Sheet
# ---------------------------------------

SHEET_ID = "18dn2ojjVdkF8QU1qTURwm3GmqOR2-eYvIn2IjGpUg4k"
GID = "980561560"


@st.cache_data(ttl=60)
def load_contacts():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"
    df = pd.read_csv(url)

    df = df.dropna(how="all")
    df = df.fillna("")

    return df


df = load_contacts()

# ---------------------------------------
# Search Box
# ---------------------------------------

search = st.text_input(
    "🔍 Search",
    placeholder="Search by brand, vendor, email, phone, notes...",
)

# ---------------------------------------
# Filter Results
# ---------------------------------------

if search:
    mask = (
        df.astype(str)
        .apply(lambda row: row.str.contains(search, case=False, na=False).any(), axis=1)
    )

    filtered = df[mask]

else:
    filtered = df

# ---------------------------------------
# Results
# ---------------------------------------

st.write(f"**Showing {len(filtered)} of {len(df)} vendors**")

st.dataframe(
    filtered,
    hide_index=True,
    use_container_width=True,
    height=850,
)
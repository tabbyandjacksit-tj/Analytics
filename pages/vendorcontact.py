import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Vendor Contacts", page_icon="📞")

st.title("📞 Vendor Contacts")
st.caption("Search for vendor representatives and contact information.")

# -----------------------
# Load Google Sheet
# -----------------------

conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=300)
def load_contacts():
    df = conn.read(
        worksheet="VENDOR CONTACT",
        usecols=list(range(20))
    )
    return df.dropna(how="all")

df = load_contacts()

# -----------------------
# Search Box
# -----------------------

search = st.text_input(
    "🔍 Search",
    placeholder="Vendor, rep, phone, email..."
)

# -----------------------
# Filter
# -----------------------

if search:
    mask = df.astype(str).apply(
        lambda col: col.str.contains(
            search,
            case=False,
            na=False
        )
    ).any(axis=1)

    filtered = df[mask]

else:
    filtered = df

# -----------------------
# Display
# -----------------------

st.write(f"Showing **{len(filtered)}** result(s)")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)
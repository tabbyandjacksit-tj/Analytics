import streamlit as st
import pandas as pd

# ---------------------------------------
# Page Styling
# ---------------------------------------

st.markdown("""
<style>
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1rem;
    max-width: 95rem;
}

.edit-box {
    margin-top: 2rem;
    padding: 20px;
    background: linear-gradient(90deg, rgba(92,128,103,.08), rgba(92,128,103,.02));
    border-left: 6px solid #5C8067;
    border-radius: 12px;
}

.edit-box h4 {
    margin: 0 0 .5rem 0;
    color: #1D5A3E;
    font-size: 1.2rem;
}

.edit-box p {
    margin: 0 0 1rem 0;
    color: #555;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# Page Header
# ---------------------------------------

st.title("☏ Vendor Contacts")
st.caption("Search vendor representatives, emails, phone numbers, and brand policies.")

# ---------------------------------------
# Google Sheet
# ---------------------------------------

SHEET_ID = "18dn2ojjVdkF8QU1qTURwm3GmqOR2-eYvIn2IjGpUg4k"
GID = "980561560"
SHEET_URL = "https://docs.google.com/spreadsheets/d/18dn2ojjVdkF8QU1qTURwm3GmqOR2-eYvIn2IjGpUg4k/edit?usp=sharing"

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
    "🔍︎ Search",
    placeholder="Search by brand, vendor, email, phone, notes...",
)

# ---------------------------------------
# Filter Results
# ---------------------------------------

if search:
    mask = df.astype(str).apply(
        lambda row: row.str.contains(search, case=False, na=False).any(),
        axis=1
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
    height=550,
)

# ---------------------------------------
# Edit Sheet Box
# ---------------------------------------

st.markdown(
    """
<div class="edit-box">
    <h4>✎ Need to add or update a vendor contact?</h4>
    <p>
        This page is search-only. Use the button below to open the editable Vendor Contact Sheet.
    </p>
</div>
""",
    unsafe_allow_html=True
)

st.link_button(
    "✎ Open Vendor Contact Sheet",
    SHEET_URL,
    use_container_width=True,
)
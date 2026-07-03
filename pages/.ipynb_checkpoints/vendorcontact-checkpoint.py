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

.table-card {
    margin-top: 1rem;
    padding: 14px;
    background-color: rgba(92, 128, 103, 0.10);
    border: 2px solid #5C8067;
    border-radius: 16px;
}

.edit-box {
    margin-top: 1.5rem;
    padding: 18px 22px;
    background-color: rgba(92, 128, 103, 0.10);
    border: 2px solid #5C8067;
    border-radius: 16px;
}

.edit-box h4 {
    margin: 0 0 .4rem 0;
    color: #1D5A3E;
}

.edit-box p {
    margin: 0;
    color: #555;
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

st.markdown('<div class="table-card">', unsafe_allow_html=True)

st.dataframe(
    filtered,
    hide_index=True,
    use_container_width=True,
    height=550,
)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------
# Edit Sheet Box
# ---------------------------------------

st.markdown(
    """
<div class="edit-box">
    <h4>✎ Looking to add or update a vendor contact?</h4>
    <p>
        This page is search-only.
        <a href="https://docs.google.com/spreadsheets/d/18dn2ojjVdkF8QU1qTURwm3GmqOR2-eYvIn2IjGpUg4k/edit?usp=sharing" target="_blank">
            Click here to edit the Vendor Contact Sheet.
        </a>
    </p>
</div>
""",
    unsafe_allow_html=True
)
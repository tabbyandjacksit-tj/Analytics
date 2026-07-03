import streamlit as st
import pandas as pd

# ---------------------------------------
# Page Config
# ---------------------------------------

st.set_page_config(
    page_title="Vendor Contact Information",
    page_icon="images/logo.png",
    layout="wide"
)

# ---------------------------------------
# Page Styling
# ---------------------------------------

st.markdown("""
<style>
footer {
    visibility: hidden;
}

[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none;
}

.stApp {
    background-color: #F6F1E5;
    color: #2F372D;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1050px;
}

.hero {
    background-color: #1D5A3E;
    padding: 28px 28px;
    border-radius: 26px;
    margin-bottom: 28px;
    box-shadow: 0px 8px 22px rgba(29,90,62,.18);
}

.hero h1 {
    text-align: center;
    color: #FFF9EF;
    font-size: 44px;
    font-weight: 800;
    margin: 0;
}

.hero p {
    text-align: center;
    color: rgba(255,249,239,0.88);
    font-size: 17px;
    margin-top: 12px;
    margin-bottom: 0;
}

.section-label {
    color: #C97822;
    font-weight: 800;
    font-size: 13px;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.section-title {
    color: #1D5A3E;
    font-size: 31px;
    font-weight: 800;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #5C7A58;
    font-size: 16px;
    margin-bottom: 20px;
}

.date-card {
    background-color: #FDF7EA;
    border: 1px solid #D7C8A4;
    border-radius: 18px;
    padding: 16px 20px;
    margin-top: 15px;
    margin-bottom: 20px;
    box-shadow: 0px 3px 10px rgba(47,55,45,0.04);
}

.date-title {
    color: #1D5A3E;
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 6px;
}

.date-text {
    color: #5C7A58;
    font-size: 14px;
    line-height: 1.6;
    margin: 0;
}

.stButton button,
.stLinkButton a {
    background-color: #C97822;
    color: white;
    border-radius: 12px;
    padding: 0.55rem 1rem;
    border: none;
    font-weight: 700;
}

.stButton button:hover,
.stLinkButton a:hover {
    background-color: #B4671C;
    color: white;
}

hr {
    border: none;
    border-top: 1px solid #D7C8A4;
    margin: 2rem 0;
}

h2, h3 {
    color: #1D5A3E;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# Page Header
# ---------------------------------------

st.markdown("""
<div class="hero">
    <h1>☏ Vendor Contacts</h1>
    <p>Search vendor representatives, emails, phone numbers, and brand policies.</p>
</div>
""", unsafe_allow_html=True)

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
# Search Section
# ---------------------------------------

st.markdown("""
<div class="section-label">Step 1</div>
<div class="section-title">Search Vendor Contacts</div>
<div class="section-subtitle">
Search by brand, vendor, email, phone number, or notes.
</div>
""", unsafe_allow_html=True)

search = st.text_input(
    "Search",
    placeholder="Search by brand, vendor, email, phone, notes...",
    label_visibility="collapsed",
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

st.markdown("---")

st.markdown("""
<div class="section-label">Step 2</div>
<div class="section-title">Results</div>
<div class="section-subtitle">
Search results update automatically from the Vendor Contact Sheet.
</div>
""", unsafe_allow_html=True)

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

st.markdown("""
<div class="date-card">
    <div class="date-title">✎ Need to add or update a vendor contact?</div>
    <p class="date-text">
        This page is search-only. Use the button below to open the editable Vendor Contact Sheet.
    </p>
</div>
""", unsafe_allow_html=True)

st.link_button(
    "✎ Open Vendor Contact Sheet",
    SHEET_URL,
    use_container_width=True,
)
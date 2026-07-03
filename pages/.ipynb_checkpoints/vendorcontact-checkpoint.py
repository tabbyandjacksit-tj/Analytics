import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Vendor Contacts",
    page_icon="images/logo.png",
    layout="wide"
)

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

h3 {
    color: #1D5A3E;
    font-size: 28px;
    font-weight: 800;
}

div[data-testid="stTextInput"] input {
    background-color: #FFF9EF;
    border: 1px solid #D7C8A4;
    border-radius: 12px;
    color: #2F372D;
}

.edit-box {
    margin-top: 1.5rem;
    padding: 18px 22px;
    background-color: #FDF7EA;
    border: 1px solid #D7C8A4;
    border-radius: 18px;
    box-shadow: 0px 3px 10px rgba(47,55,45,0.04);
}

.edit-box h4 {
    margin: 0 0 .4rem 0;
    color: #1D5A3E;
}

.edit-box p {
    margin: 0;
    color: #5C7A58;
}

.stLinkButton a {
    background-color: #1D5A3E;
    color: white;
    border-radius: 12px;
    font-weight: 700;
}

.stLinkButton a:hover {
    background-color: #15442F;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>☏ Vendor Contacts</h1>
    <p>Search vendor representatives, emails, phone numbers, and brand policies.</p>
</div>
""", unsafe_allow_html=True)

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

st.markdown("### Search Vendor Contacts")

search = st.text_input(
    "Search",
    placeholder="Search by brand, vendor, email, phone, notes...",
    label_visibility="collapsed"
)

if search:
    mask = df.astype(str).apply(
        lambda row: row.str.contains(search, case=False, na=False).any(),
        axis=1
    )
    filtered = df[mask]
else:
    filtered = df

st.write(f"**Showing {len(filtered)} of {len(df)} vendors**")

st.dataframe(
    filtered,
    hide_index=True,
    use_container_width=True,
    height=550,
)

st.markdown("""
<div class="edit-box">
    <h4>✎ Looking to add or update a vendor contact?</h4>
    <p>This page is search-only. Use the button below to open the editable Vendor Contact Sheet.</p>
</div>
""", unsafe_allow_html=True)

st.link_button(
    "✎ Open Vendor Contact Sheet",
    SHEET_URL,
    use_container_width=True,
)
import streamlit as st
import pandas as pd

from utils.styling import apply_base_styles, render_hero, apply_extra_css

st.set_page_config(
    page_title="Vendor Contacts",
    page_icon="images/logo.png",
    layout="wide"
)

apply_base_styles()

apply_extra_css(
    """
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
"""
)

render_hero(
    "☏ Vendor Contacts",
    "Search for reps, emails, and expiration policies.",
)

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
    filtered = df[mask].copy()
else:
    filtered = df.copy()

st.write(f"**Showing {len(filtered)} of {len(df)} vendors**")

checkbox_cols = [
    "Credit back?",
    "Replacements?",
    "Case-by-Case Basis?"
]

for col in checkbox_cols:
    if col in filtered.columns:
        filtered[col] = (
            filtered[col]
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["true", "yes", "1", "checked"])
        )

st.dataframe(
    filtered,
    hide_index=True,
    use_container_width=True,
    height=550,
    column_config={
        "Credit back?": st.column_config.CheckboxColumn("Credit back?"),
        "Replacements?": st.column_config.CheckboxColumn("Replacements?"),
        "Case-by-Case Basis?": st.column_config.CheckboxColumn("Case-by-Case Basis?"),
    }
)

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
#  {forestGreen,7} =====================================================================
# Imports
# =======================================================================================
import pandas as pd
import streamlit as st
from utils.styling.base import apply_base_styles, render_hero
from utils.styling.vendor import apply_vendor_styles, render_edit_box
from utils.sheet_reader import load_sheet
#  {yellowgreen,7} =====================================================================
# Page Configuration (sets title, icon, and layout of page)
# =======================================================================================
st.set_page_config(
    page_title="MAP Information",
    page_icon="images/logo.png",
    layout="wide",
)
# {yellowgreen, 8} =======================================================================================
# Apply CSS Styles
# =======================================================================================
apply_base_styles()
apply_vendor_styles()
render_hero(
    "☏ MAP Information",
    "Search for which vendors follow MAP pricing, and what their pricing might be!",
)

# =======================================================================================
# Initialize variables for the google sheet & checkbox columns
# =======================================================================================
SHEET_ID = "1jEMzkdoDlyFqdYH0YjBy4yMfza1-8XrJOnkCzhg88xM"
BRAND_GID = "0"
TOTAL_GID = "1566617171"

BRAND_DF = load_sheet(SHEET_ID, BRAND_GID)
TOTAL_DF = load_sheet(SHEET_ID, TOTAL_GID)


st.markdown("### Search MAP Information")
search = st.text_input(
    "Search",
    placeholder="Search by brand, vendor, email, phone, notes...",
    label_visibility="collapsed",
)
if search:
    mask = BRAND_DF.astype(str).apply(
        lambda row: row.str.contains(search, case=False, na=False).any(),
        axis=1,
    )
    brand_filtered = BRAND_DF[mask].copy()
else:
    brand_filtered = BRAND_DF.copy()
st.write(f"**Showing {len(brand_filtered)} of {len(BRAND_DF)} vendors**")

st.dataframe(
    brand_filtered,
    hide_index=True,
    use_container_width=True,
    height=550,
)

st.markdown("### Search for a products MAP price")
search = st.text_input(
    "Search",
    placeholder="Search by brand, vendor, email, phone, notes...",
    label_visibility="collapsed",
)
if search:
    mask = TOTAL_DF.astype(str).apply(
        lambda row: row.str.contains(search, case=False, na=False).any(),
        axis=1,
    )
    total_filtered = TOTAL_DF[mask].copy()
else:
    total_filtered = TOTAL_DF.copy()
st.write(f"**Showing {len(total_filtered)} of {len(TOTAL_DF)} vendors**")

st.dataframe(
    total_filtered,
    hide_index=True,
    use_container_width=True,
    height=550,
) 
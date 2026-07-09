#  {forestGreen,8} =====================================================================
# Imports
# =======================================================================================
import pandas as pd
import streamlit as st
from utils.styling.base import apply_base_styles, render_hero
from utils.sheet_reader import load_sheet
from utils.styling.vendor import apply_vendor_styles, render_edit_box, render_map_section
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


render_map_section(
    "Search For Details About MAP Pricing",
    "See if a brand follows the MAP pricing, when it was last updated on Lightspeed, and what the policy is for each brand.",
)
search = st.text_input(
    "Search",
    placeholder="Search brands....",
    label_visibility="collapsed",
    key = "brand_search",
)
if search:
    mask = BRAND_DF.astype(str).apply(
        lambda row: row.str.contains(search, case=False, na=False).any(),
        axis=1,
    )
    brand_filtered = BRAND_DF[mask].copy()
else:
    brand_filtered = BRAND_DF.copy()
brand_filtered = brand_filtered.drop(columns=["Hide"])
st.dataframe(
    brand_filtered,
    hide_index=True,
    use_container_width=True,
    height=200,
)


render_map_section(
    "Search Product Pricing Details",
    "Check what the MAP pricing is for each product, and when it is was last updated by the vendor."
)
search = st.text_input(
    "Search",
    placeholder="Search by brand, UPC, or item name....",
    label_visibility="collapsed",
    key = "total_search",
)
if search:
    mask = TOTAL_DF.astype(str).apply(
        lambda row: row.str.contains(search, case=False, na=False).any(),
        axis=1,
    )
    total_filtered = TOTAL_DF[mask].copy()
else:
    total_filtered = TOTAL_DF.copy()
st.dataframe(
    total_filtered,
    hide_index=True,
    use_container_width=True,
    height=750,
) 
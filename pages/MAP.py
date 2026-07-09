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
st.dataframe(BRAND_DF, use_container_width=True, hidden_index = True)

st.markdown("### Search for a products MAP price")
st.dataframe(TOTAL_DF, use_container_width=True, hidden_index = True)   
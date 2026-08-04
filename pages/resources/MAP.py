# =======================================================================================
# Imports
# =======================================================================================
import streamlit as st
from utils.components.headers import render_section_header
from utils.styling.base import (
    apply_base_styles,
    render_hero,
)
from utils.styling.components import apply_component_styles
from utils.styling.vendor import apply_vendor_styles
from utils.tools.sheet_reader import load_sheet
from utils.tools.navigation import render_breadcrumb
# =======================================================================================
# Page Configuration (sets title, icon, and layout of page)
# CSS Styles also imported/applied
# =======================================================================================
st.set_page_config(
    page_title="MAP Information",
    page_icon="images/logo.png",
    layout="wide",
)
apply_base_styles()
apply_component_styles()
apply_vendor_styles()
render_breadcrumb(__file__)
render_hero(
    "MAP Information",
    (
        "Search brand MAP policies and verify compliant "
        "product pricing."
    ),
)
# =======================================================================================
# Initialize variables for the google sheet & checkbox columns. This is basically copied from 
# vendorcontact.py, but adjusted to be MAP since it is a bit more! 
# =======================================================================================
SHEET_ID = "1jEMzkdoDlyFqdYH0YjBy4yMfza1-8XrJOnkCzhg88xM"
BRAND_GID = "0"
TOTAL_GID = "1566617171"

BRAND_DF = load_sheet(SHEET_ID, BRAND_GID)
TOTAL_DF = load_sheet(SHEET_ID, TOTAL_GID)
# =======================================================================================
# Creates a section to search for which brands follow MAP pricing. If a brand follows MAP, 
# than the table will show the brand and when they last updated if that info is avaliable to me. 
# Master copy is kept in TabbyandjacksIT@gmail.com
# =======================================================================================
render_section_header(
    label="Brand Policies",
    title="Search MAP Policy Details",
    subtitle=(
        "Check whether a brand follows MAP pricing, review its "
        "policy details, and see when the information was last updated."
    ),
)
# Creates the search section  and spits out if the brand is MAP or not!  
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
brand_filtered = brand_filtered.drop(
    columns=["Hide"],
    errors="ignore",
)
st.dataframe(
    brand_filtered,
    hide_index=True,
    use_container_width=True,
    height=200,
)
# =======================================================================================
# Creates a section to search for a products MAP pricing,
# The idea is that the user is able to enter a name or a UPC, and what it should be priced comes out. 
# Master copy is kept in TabbyandjacksIT@gmail.com
# =======================================================================================
render_section_header(
    label="Product Pricing",
    title="Search MAP Product Pricing",
    subtitle=(
        "Search by brand, UPC, or item name to verify the "
        "current MAP price."
    ),
)
# Creates the search section  and says what to price at when/if that is found in the data system. 
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
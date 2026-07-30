
# TODO: This will eventually be equivalent to the sale by brand report in Analytics.

# =======================================================================================
# Imports
# =======================================================================================
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
from utils.reporting.mvo import calculate_order_quantities, find_missing_columns
from utils.styling.base import apply_base_styles, render_hero
from utils.styling.mvo import (
    apply_mvo_styles,
    render_date_card,
    render_instruction_card,
    render_preview_title,
)
from utils.components.headers import render_section_header
# =======================================================================================
# Page Configuration (sets title, icon, and layout of page)
# CSS Styles also imported/applied
# =======================================================================================
st.set_page_config(
    page_title="Sales by Brand",
    page_icon="images/logo.png",
    layout="wide",
)
apply_base_styles()
apply_mvo_styles()
render_hero(
    "Sales by Brand",
    "See the sales per brand based on the sales and set time",
)
# =======================================================================================
# Creates the instructions for exporting the report from Lightspeed in step 1.
# Each step has an image, title, and description.
# =======================================================================================
render_section_header(
    title = "Export Report from Lightspeed",
    subtitle = "Follow these steps to export the correct CSV report for analysis.",
)
steps = [
    ("images/reports.png", "Reports", "Open REPORTS from the sidebar."),
    ("images/grouped_sales.png", "Grouped Sales", "Scroll to GROUPED SALES TOTAL."),
    ("images/item_report.png", "Item Report", "Select ITEM as the report type."),
    ("images/calendar.png", "Date Filter", "Set DATE RANGE based on report frequency below."),
    ("images/vendor.png", "Brand Filter", "Choose the desired BRAND."),
    ("images/export.png", "Export CSV", "Press EXPORT and save the CSV."),
]
row1 = st.columns(3)
for i, step in enumerate(steps[:3]):
    with row1[i]:
        render_instruction_card(i + 1, *step)
st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
row2 = st.columns(3)
for i, step in enumerate(steps[3:]):
    with row2[i]:
        render_instruction_card(i + 4, *step)
# =======================================================================================
# Calculates and creates a box for the dates that are 56 days out, or weekly which is 28 
# =======================================================================================
days_ago = st.number_input(
    "Enter the number of days for your report",
    min_value=1,
    value=90,
    step=1,
)
calculated_date = datetime.today() - timedelta(days=days_ago)
st.info(
    f"Start your report on "
    f"**{calculated_date.strftime('%B %d, %Y')}** "
    f"for a {days_ago}-day date range."
)







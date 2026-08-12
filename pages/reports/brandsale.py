
# TODO: This will eventually be equivalent to the sale by brand report in Analytics.

# =======================================================================================
# Imports
# =======================================================================================
from datetime import datetime, timedelta
import streamlit as st
from utils.components.headers import (
    render_section_header,
    render_subsection_header,
)
from utils.components.cards import (render_instruction_card, render_instruction_grid,)
from utils.styling.base import (apply_base_styles, render_hero,)
from utils.styling.components import (apply_component_styles, apply_instruction_styles,)
from utils.styling.mvo import (
    apply_mvo_styles,
)
from utils.tools.navigation import render_breadcrumb
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
apply_component_styles()
apply_instruction_styles()
apply_mvo_styles()
render_breadcrumb(__file__)
render_hero(
    "Sales by Brand",
    (
        "Review sales performance for a selected brand "
        "and date range."
    ),
)
# =======================================================================================
# Creates the instructions for exporting the report from Lightspeed in step 1.
# Each step has an image, title, and description.
# =======================================================================================
render_section_header(
    label="Step 1",
    title="Export Report from Lightspeed",
    subtitle=(
        "Follow these steps to export the correct grouped sales "
        "report for analysis."
    ),
)

steps = [
    (
    "Reports",
    "Open REPORTS from the sidebar.",
    "images/reports.png",
    ),
    ("Grouped Sales","Scroll to GROUPED SALES TOTAL.","images/grouped_sales.png",),
    ("Item Report","Select ITEM as the report type.","images/item_report.png",),
    ("Date Filter","Set DATE RANGE based on report frequency below.","images/calendar.png",),
    ("Brand Filter","Choose the desired BRAND.","images/vendor.png",),
    ("Export CSV","Press EXPORT and save the CSV.","images/export.png",
    ),
    ]

render_instruction_grid(
    steps,
    columns_per_row=3,
)
# =======================================================================================
# Calculates and creates a box for the dates that are 56 days out, or weekly which is 28 
# =======================================================================================
render_section_header(
    label="Step 2",
    title="Choose the Report Date Range",
    subtitle=(
        "Enter the number of days you would like to include "
        "in the sales report."
    ),
)
days_ago = st.number_input(
    "Number of Days",
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







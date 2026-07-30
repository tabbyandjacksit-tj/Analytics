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
    page_title="Major Vendor Order",
    page_icon="images/logo.png",
    layout="wide",
)
apply_base_styles()
apply_mvo_styles()
render_hero(
    "Major Vendor Order Report",
    "Generate a vendor order from a Lightspeed item sales report.",
)
# =======================================================================================
# Creates the instructions for exporting the report from Lightspeed in step 1.
# Each step has an image, title, and description.
# =======================================================================================
render_section_header(
    eyebrow = "Step 1",
    title = "Export Report from Lightspeed",
    subtitle = "Follow these steps to export the correct CSV report.",
)
steps = [
    ("images/reports.png", "Reports", "Open REPORTS from the sidebar."),
    ("images/grouped_sales.png", "Grouped Sales", "Scroll to GROUPED SALES TOTAL."),
    ("images/item_report.png", "Item Report", "Select ITEM as the report type."),
    ("images/calendar.png", "Date Filter", "Set DATE RANGE based on report frequency below."),
    ("images/vendor.png", "Vendor Filter", "Choose the desired VENDOR."),
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
bi_report_start = datetime.today() - timedelta(days=56) 
weekly_report_start = datetime.today() - timedelta(days=28) 
render_date_card(bi_report_start, weekly_report_start) 
render_section_header(
    eyebrow = "Step 2",
    title = "Upload Item Sale Report",
)
# ======================================================
# Upload the Lightspeed Item report & check for missing columns and other potential errors
# ======================================================
uploaded_file = st.file_uploader(
    "Upload Lightspeed CSV",
    type=["csv"],
    label_visibility="collapsed",
)
st.caption("Please use only the CSV exported directly from Lightspeed. Do not edit or open file.")
st.divider()
if uploaded_file is None:
    st.stop()
df = pd.read_csv(uploaded_file)
missing_columns = find_missing_columns(df)
if missing_columns:
    st.error(
        "It appears that you may have uploaded the wrong file! "
        f"Your file must contain these columns: {', '.join(missing_columns)}"
    )
    st.stop()
# =======================================================================================
# Manipulates the uploaded report and calculates the order quantities based on utils.mvo
# =======================================================================================
output_df = calculate_order_quantities(df)
render_section_header(
    eyebrow = "Step 3",
    title = "Order Results",
    subtitle = "Review the recommended order quantities below, and download your CSV.",
)
render_preview_title()
st.dataframe(output_df.head(50), use_container_width=True) # Previews the first 50 rows of the MVO
full_csv = output_df.to_csv(index=False) # Creates a CSV of the full MVO output for download
# Only gathers the UPC and Order QTY columns and copies them into a dataframe. 
upc_order_df = output_df[["UPC", "Order Qty"]].copy()
upc_order_csv = upc_order_df.to_csv(index=False)
# Gives a warning that the file should not be opened, bc the CSV might be remove leading 0's 
@st.dialog("Heads up!")
def order_template_warning():
    st.write(
        "ⓘ **Heads up!** Please **do not** open this file. "
        "Instead, import it directly into a Lightspeed Purchase Order."
    )
    # Creatres the download button for the order template. 
    st.download_button(
        label="Download Order Template",
        data=upc_order_csv,
        file_name="upc_order_template.csv",
        mime="text/csv",
        use_container_width=True,
    )
# =======================================================================================
# Creates the download buttons for the full CSV and order template, 
# and gives a warning about what to do after downloading. Also sets the spacing for the buttons
# =======================================================================================
left, right = st.columns(2)
with left:
    # Creates the dowload button for the entire CSV incase there is an error. 
    st.download_button(
        label="Download Unedited CSV",
        data=full_csv,
        file_name="major_vendor_order_output.csv",
        mime="text/csv",
        use_container_width=True,
    )
with right: 
    # Creates the dowload button for just the order template
    if st.button("Download Order Template", use_container_width=True):
        order_template_warning()

# Provides an alert message that the DISCO items will need to be removed, since LS does not give report with VendorID. 
st.markdown(
    "ⓘ **Heads Up!** After importing into Lightspeed, remove any discontinued items and any items with a blank Vendor ID."
)
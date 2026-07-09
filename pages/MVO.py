from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from utils.mvo import calculate_order_quantities, find_missing_columns
from utils.styling.base import apply_base_styles, render_hero
from utils.styling.mvo import (
    apply_mvo_styles,
    render_date_card,
    render_instruction_card,
    render_preview_title,
    section_header,
)

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

section_header(
    "Step 1",
    "Export Report from Lightspeed",
    "Follow these steps to export the correct CSV report.",
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

bi_report_start = datetime.today() - timedelta(days=56)
weekly_report_start = datetime.today() - timedelta(days=28)

render_date_card(bi_report_start, weekly_report_start)

section_header(
    "Step 2",
    "Upload Item Sale Report",
)

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

output_df = calculate_order_quantities(df)

section_header(
    "Step 3",
    "Order Results",
    "Review the recommended order quantities below, and download your CSV.",
)

render_preview_title()

st.dataframe(output_df.head(50), use_container_width=True)

full_csv = output_df.to_csv(index=False)

upc_order_df = output_df[["UPC", "Order Qty"]].copy()
upc_order_csv = upc_order_df.to_csv(index=False)


@st.dialog("Heads up!")
def order_template_warning():
    st.write(
        "ⓘ **Heads up!** Please **do not** open this file. "
        "Instead, import it directly into a Lightspeed Purchase Order."
    )

    st.download_button(
        label="Download Order Template",
        data=upc_order_csv,
        file_name="upc_order_template.csv",
        mime="text/csv",
        use_container_width=True,
    )


left, spacer, right = st.columns([2, 8, 2])

with left:
    st.download_button(
        label="Download Unedited CSV",
        data=full_csv,
        file_name="major_vendor_order_output.csv",
        mime="text/csv",
        use_container_width=True,
    )

with right:
    if st.button("Download Order Template", use_container_width=True):
        order_template_warning()

st.markdown(
    "ⓘ **Heads Up!** After importing into Lightspeed, remove any discontinued items and any items with a blank Vendor ID."
)
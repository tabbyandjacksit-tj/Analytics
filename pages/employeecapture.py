import pandas as pd
import streamlit as st

from utils.employee_capture import (
    find_missing_columns,
    prepare_employee_report,
    summarize_employee_capture,
)
from utils.styling.base import apply_base_styles, render_hero
from utils.styling.mvo import (
    apply_mvo_styles,
    render_instruction_card,
    section_header,
)

st.set_page_config(
    page_title="Employee Customer Capture",
    page_icon="images/logo.png",
    layout="wide",
)

apply_base_styles()
apply_mvo_styles()

render_hero(
    "Employee Customer Capture",
    "Review how often an employee attaches a customer to completed sales.",
)

steps = [
    ("images/reports.png", "Reports", "Open REPORTS from the sidebar."),
    ("images/grouped_sales.png", "Grouped Sales", "Scroll to OTHER TRANSACTIONS."),
    ("images/item_report.png", "All Transactions", "Select ALL TRANSACTIONS as the report type."),
    ("images/calendar.png", "Date Filter", "Set DATE RANGE to what you hope to review."),
    ("images/export.png", "Export CSV", "Press EXPORT and save the CSV."),
    ("images/upload.png", "Upload CSV", "Upload the exported CSV file below."),
]

section_header(
    "Step 1",
    "Export the Employee Capture Report",
    "Follow these steps to prepare the correct CSV file.",
)

row1 = st.columns(3)

for index, step in enumerate(steps[:3]):
    with row1[index]:
        render_instruction_card(index + 1, *step)

st.markdown(
    "<div style='height:12px;'></div>",
    unsafe_allow_html=True,
)

row2 = st.columns(3)

for index, step in enumerate(steps[3:]):
    with row2[index]:
        render_instruction_card(index + 4, *step)


# =============================================================================
# FILE UPLOAD
# =============================================================================

uploaded_file = st.file_uploader(
    "Upload Employee Report",
    type=["csv"],
)

if uploaded_file is None:
    section_header(
        "Step 1",
        "Export Employee Capture Report",
        "Follow these steps to generate the correct CSV report.",
    )

    render_instruction_card(steps)

    st.divider()
    st.stop()

# =============================================================================
# REPORT VALIDATION
# =============================================================================

try:
    report_df = pd.read_csv(uploaded_file)
except Exception as error:
    st.error(f"Could not read the uploaded CSV: {error}")
    st.stop()

missing_columns = find_missing_columns(report_df)

if missing_columns:
    st.error(
        "The uploaded report is missing these required columns: "
        f"{', '.join(missing_columns)}"
    )
    st.stop()

cleaned_df = prepare_employee_report(report_df)


# =============================================================================
# EMPLOYEE SELECTION
# =============================================================================

employees = sorted(
    employee
    for employee in cleaned_df["Employee"].unique()
    if employee
)

if not employees:
    st.warning("No employees were found in the uploaded report.")
    st.stop()

selected_employee = st.selectbox(
    "Select Employee",
    options=employees,
)


# =============================================================================
# CUSTOMER CAPTURE RESULTS
# =============================================================================

results = summarize_employee_capture(
    cleaned_df,
    selected_employee,
)

total_sales = results["total_sales"]
attached_sales = results["attached_sales"]
unattached_sales = results["unattached_sales"]
capture_rate = results["capture_rate"]
employee_df = results["employee_df"]

st.markdown(f"### Results for {selected_employee}")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", total_sales)
col2.metric("Customer Attached", attached_sales)
col3.metric("No Customer Attached", unattached_sales)
col4.metric("Capture Rate", f"{capture_rate:.1%}")


# =============================================================================
# TRANSACTION DETAILS
# =============================================================================

display_df = employee_df[
    [
        "ID",
        "Date",
        "Shop",
        "Register",
        "Total",
        "Customer",
        "Customer Attached",
        "Source",
    ]
].copy()

st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True,
)
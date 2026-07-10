import pandas as pd
import streamlit as st

from utils.employee_capture import (
    find_missing_columns,
    prepare_employee_report,
    summarize_employee_capture,
)
from utils.styling.base import apply_base_styles, render_hero


st.set_page_config(
    page_title="Employee Customer Capture",
    page_icon="images/logo.png",
    layout="wide",
)

apply_base_styles()

render_hero(
    "Employee Customer Capture",
    "Review how often an employee attaches a customer to completed sales.",
)


# =============================================================================
# FILE UPLOAD
# =============================================================================

uploaded_file = st.file_uploader(
    "Upload Transaction Report",
    type=["csv"],
)

if uploaded_file is None:
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
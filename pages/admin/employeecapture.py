# =======================================================================================
# Imports
# =======================================================================================
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from utils.components.headers import (
    render_section_header,
    render_subsection_header,
)
from utils.styling.base import (
    apply_base_styles,
    render_hero,
)
from utils.styling.components import apply_component_styles
from utils.styling.mvo import (
    apply_mvo_styles,
    render_instruction_card,
)
from utils.reporting.employee_capture import (
    employee_leaderboard,
    find_missing_columns,
    prepare_employee_report,
    summarize_employee_capture,
)
from utils.tools.navigation import render_breadcrumb


st.set_page_config(
    page_title="Employee Customer Capture",
    page_icon="images/logo.png",
    layout="wide",
)
apply_base_styles()
apply_component_styles()
apply_mvo_styles()
render_breadcrumb(__file__)
render_hero(
    "Employee Customer Capture",
    "Review how often an employee attaches a customer to completed sales.",
)
# =============================================================================
# FILE UPLOAD
# =============================================================================
render_section_header(
    label="Step 1",
    title="Upload Employee Capture Report",
    subtitle=(
        "Upload the completed transaction report exported "
        "from Lightspeed."
    ),
)

with st.container(border=True):

    left, right = st.columns([3, 1])

    with left:
        uploaded_file = st.file_uploader(
            "Upload Employee Report",
            type=["csv"],
            label_visibility="collapsed",
        )

    with right:
        days_ago = st.number_input(
            "Number of Days",
            min_value=1,
            value=90,
            step=1,
        )

        calculated_date = datetime.today() - timedelta(days=days_ago)

        st.caption(
            f"Start Report: **{calculated_date:%b %d, %Y}**"
        )

if uploaded_file is None:
    steps = [
        ("images/reports.png", "Reports", "Open REPORTS from the sidebar."),
        ("images/grouped_sales.png", "Other Transactions", "Scroll to OTHER TRANSACTIONS."),
        ("images/item_report.png", "All Transactions", "Select ALL TRANSACTIONS as the report type."),
        ("images/calendar.png", "Date Filter", "Set DATE RANGE to what you hope to review."),
        ("images/export.png", "Export CSV", "Press EXPORT and save the CSV."),
        ("images/upload.png", "Upload CSV", "Upload the exported CSV file below."),
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
# Creates a leaderboard of the top 10 employee capture rates, as long as they have 
# had over 15 sales in the given time frame. 
# =============================================================================
# =============================================================================
# EMPLOYEE LEADERBOARD
# =============================================================================

leaderboard_df = employee_leaderboard(cleaned_df)

leaderboard_df = leaderboard_df[
    leaderboard_df["Completed Sales"] >= 15
].head(10)

render_section_header(
    label="Top 10",
    title="Employee Customer Capture Rates",
    subtitle=(
        "Employees must have at least 15 completed sales "
        "to qualify."
    ),
)

if leaderboard_df.empty:
    st.info(
        "No employees had at least 15 completed sales "
        "in this report."
    )
else:
    leaderboard_df["Capture Rate"] = (
        leaderboard_df["Capture Rate"] * 100
    ).round(1)

    st.dataframe(
        leaderboard_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Capture Rate": st.column_config.NumberColumn(
                "Capture Rate",
                format="%.1f%%",
            ),
        },
    )
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
render_section_header(
    label="Step 2",
    title="Select an Employee",
    subtitle=(
        "Choose an employee to review their customer capture "
        "performance."
    ),
)
selected_employee = st.selectbox("Select Employee", options=employees,)
# =============================================================================
# CUSTOMER CAPTURE RESULTS
# =============================================================================
results = summarize_employee_capture(cleaned_df, selected_employee,)
total_sales = results["total_sales"]
attached_sales = results["attached_sales"]
unattached_sales = results["unattached_sales"]
capture_rate = results["capture_rate"]
employee_df = results["employee_df"]
render_section_header(
    label="Employee Results",
    title=f"Results for {selected_employee}",
    subtitle=(
        "Review completed sales and the percentage of transactions "
        "with an attached customer."
    ),
)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", total_sales)
col2.metric("Customer Attached", attached_sales)
col3.metric("No Customer Attached", unattached_sales)
col4.metric("Capture Rate", f"{capture_rate:.1%}")
# =============================================================================
# TRANSACTION DETAILS
# =============================================================================
render_subsection_header(
    title="Transaction Details",
    subtitle=(
        "Review each completed transaction included in the "
        "employee's results."
    ),
)
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

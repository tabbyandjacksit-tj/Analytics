# =======================================================================================
# Imports
# =======================================================================================
import pandas as pd
import streamlit as st
from utils.components.headers import (render_section_header, render_subsection_header,)
from utils.components.cards import (
    render_instruction_grid,
    render_upload_date_card,
)
from utils.styling.components import (
    apply_component_styles,
    apply_instruction_styles,
)
from utils.styling.base import (apply_base_styles, render_hero,)
from utils.reporting.employee_capture import (employee_leaderboard, find_missing_columns, get_employee_names, prepare_employee_report, summarize_employee_capture,)
from utils.tools.navigation import render_breadcrumb
from utils.styling.mvo import (apply_mvo_styles)
# =======================================================================================
# Apply Styling & Render Hero
# =======================================================================================
st.set_page_config(
    page_title="Employee Customer Capture",
        page_icon="images/logo.png",
        layout="wide",
    )
apply_base_styles()
apply_instruction_styles()
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
render_section_header( # Creates the seciton titling for where you upload the report
    hide_label=True,
    title="Upload Employee Capture Report",
    subtitle=(
        "Upload the completed transaction report exported "
        "from Lightspeed."
    ),
)
# Creates a side-by-side layout for file upload & date selection.
uploaded_file, days_ago, calculated_date = render_upload_date_card( 
    upload_label="Upload Employee Report",
    file_types=["csv"],
    default_days=90,
)

# =============================================================================
# INSTRUCTION CARDS
# =============================================================================
if uploaded_file is None:
    steps = [
        (
            
            "Reports",
            "Open REPORTS from the sidebar.",
            "images/reports.png",
        ),
        (
            "Other Transactions",
            "Scroll to OTHER TRANSACTIONS.",
            "images/grouped_sales.png",
        ),
        (
            "All Transactions",
            "Select ALL TRANSACTIONS as the report type.",
            "images/item_report.png",
        ),
        (
            "Date Filter",
            "Set DATE RANGE to what you hope to review.",
            "images/calendar.png",
        ),
        (
            "Export CSV",
            "Press EXPORT and save the CSV.",
            "images/export.png",
        ),
        (
            "Upload CSV",
            "Upload the exported CSV file above.",
            "images/upload.png",
        ),
    ]

    render_instruction_grid(
        steps,
        columns_per_row=3,
    )
    # Puts the instruction cards into two rows of three cards each.
    st.stop()
# =============================================================================
# ENSURE THAT THE REPORT IS READABLE AND HAS ALL REQUIRED COLUMNS
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

leaderboard_df = employee_leaderboard(
    cleaned_df,
    min_sales=15,
    limit=10,
)

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
        "No employees have at least 15 completed sales in the selected time frame."
    )
else:
    # Calculate the capture rate as a percentage and round to one decimal place for display.
    leaderboard_df["Capture Rate"] = (leaderboard_df["Capture Rate"] * 100).round(1)
    st.dataframe( # display the leaderboard dataframe in a table format
        leaderboard_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Capture Rate": st.column_config.NumberColumn("Capture Rate",format="%.1f%%",),
        },
    )
# =============================================================================
# EMPLOYEE SELECTION
# =============================================================================
employees = get_employee_names(cleaned_df)
if not employees: # there needs to be employees to run calculations on, if not, it will stop the program and display a warning message.
    st.warning("No employees were found in the uploaded report.")
    st.stop()
render_section_header( # creates the titling for selecting an employee 
    hide_label=True,
    title="Select an Employee",
    subtitle=(
        "Choose an employee to review their customer capture "
        "performance."
    ),
) 
#Create a dropdown/select menu to choose an employee from the list of employees in the report.
selected_employee = st.selectbox("Select Employee", options=employees,) 
# =============================================================================
# CUSTOMER CAPTURE RESULTS
# Summarizes the employee capture results and displays the total sales,
# attached sales, unattached sales, and capture rate in a metric format. 
# It also displays a dataframe of the employee's completed transactions.
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
col1, col2, col3, col4 = st.columns(4) # Creates/lists in col form
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
display_df = employee_df[ # Diplays a dataframe of the employee's completed transactions, but only shows the following columns.
    [
        "ID",
        "Date",
        "Shop",
        "Register",
        "Total",
        "Customer",
        "Customer Attached",
        "Source",
    ]].copy()
st.dataframe(display_df, hide_index=True, use_container_width=True,)

import streamlit as st
import pandas as pd
from io import BytesIO

from utils.styling.base import apply_base_styles, render_hero
from utils.components.headers import render_section_header
from utils.tools.navigation import render_breadcrumb
from utils.styling.components import (
    apply_component_styles,
    apply_instruction_styles,
)
from utils.components.cards import (
    render_instruction_grid,
    render_upload_date_card,
    render_upload_report_button,
)
from utils.styling.mvo import (apply_mvo_styles)

# =============================================================================
# Page Configuration
# =============================================================================

st.set_page_config(
    page_title="Sort Grooming",
    page_icon="images/logo.png",
    layout="wide",
)

apply_base_styles()
apply_instruction_styles()
apply_component_styles()
apply_mvo_styles()
render_breadcrumb(__file__)

render_hero(
    "Grooming Appointment Sorter",
    (
        "Find appointments that were booked during an employee's "
        "scheduled work dates and locations."
    ),
)


# =============================================================================
# INSTRUCTION CARDS
# =============================================================================

render_section_header(
    title="Obtain the Grooming Report from MoeGo",
    subtitle="Access MoeGo and export the appointments booked report.",
)

number_of_days = 90  # Default number of days to look back for the report
render_upload_report_button(
    report_url="https://go.moego.pet/report/insights/reports?diagramId=reports_appointment_list&active=6&%7Ec=611&%7Eb=114082",
    days_ago=number_of_days,
    button_label="Open MoeGo Report",
)


# =============================================================================
# Step 1: Upload Report
# =============================================================================
# UPLOAD REPORT: Change the date range to be as many days ago as you want it to start TO 180 days from now. Than select download!

render_section_header( # Creates the seciton titling for where you upload the report
    hide_label=True,
    title="Upload Grooming Report",
    subtitle=(
        "Upload the appointments booked report exported from MoeGo."
    ),
)

uploaded_file, days_ago, calculated_date = render_upload_date_card( 
    upload_label="Upload Grooming Report",
    file_types=["csv"],
    default_days=90,
)



# =============================================================================
# Load Report
# =============================================================================

try:
    df = pd.read_csv(uploaded_file)
except Exception as error:
    st.error(f"Unable to read the uploaded CSV file: {error}")
    st.stop()


# =============================================================================
# Validate Required Columns
# =============================================================================

required_columns = [
    "Create date",
    "Create by",
    "First name",
    "Last name",
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "The uploaded report is missing these required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()


# =============================================================================
# Remove Unneeded Columns
# =============================================================================

remove_columns = [
    "Invoice ID",
    "Booking ID",
    "Client ID",
    "Pet name",
    "Service",
    "Full address",
    "Add ons",
    "Pets & services",
    "Service charges",
    "Expected revenue",
    "Collected service price",
    "Collected service charge",
    "Collected product price",
    "Collected tips",
    "Collected tax",
    "Unpaid revenue",
    "Tips",
    "Taxes",
    "Discount",
    "Payment",
    "Refund",
    "Net sale",
    "Alert note",
    "Status",
    "Payment status",
    "Time",
    "Staffs",
]

df = df.drop(
    columns=[
        column
        for column in remove_columns
        if column in df.columns
    ]
)


# =============================================================================
# Rename Booking Information
# =============================================================================

df = df.rename(
    columns={
        "Create date": "Booking Date",
        "Create by": "Booking Location",
    }
)


# =============================================================================
# Clean Booking Date
# =============================================================================

df["Booking Date"] = pd.to_datetime(
    df["Booking Date"],
    errors="coerce",
).dt.date

df["Booking Location"] = (
    df["Booking Location"]
    .astype("string")
    .str.strip()
)


# Remove rows without usable booking information
df = df[
    df["Booking Date"].notna()
    & df["Booking Location"].notna()
].copy()

df = df.drop_duplicates()


# =============================================================================
# Clean Appointment Date
# =============================================================================

# MoeGo may call the actual appointment date either "Date" or "Booked".
appointment_date_column = None

if "Date" in df.columns:
    appointment_date_column = "Date"

elif "Booked" in df.columns:
    appointment_date_column = "Booked"

if appointment_date_column is not None:
    df[appointment_date_column] = pd.to_datetime(
        df[appointment_date_column],
        errors="coerce",
    ).dt.date


# =============================================================================
# Step 2: Employee Schedule
# =============================================================================

render_section_header(
    label="Step 2",
    title="Select Employee Schedule",
)

locations = [
    "Sun Prairie Front desk",
    "Middleton Front desk",
    "East Washington Ave Retail",
    "Fitchburg Front Desk",
    "Stoughton Front Desk",
    "Oregon Front Desk",
    "Monona Drive Front Desk",
    "Verona Front Desk",
    "Cross Plains Front Desk",
]

if "work_days" not in st.session_state:
    st.session_state.work_days = []

if "results" not in st.session_state:
    st.session_state.results = None


schedule_column_1, schedule_column_2 = st.columns(2)

with schedule_column_1:
    new_date = st.date_input(
        "Employee Work Date",
    )

with schedule_column_2:
    location = st.selectbox(
        "Employee Work Location",
        locations,
    )


button_column_1, button_column_2 = st.columns(2)

with button_column_1:
    if st.button(
        "Add Work Day",
        use_container_width=True,
    ):
        new_work_day = {
            "Work Date": new_date,
            "Work Location": location,
        }

        if new_work_day not in st.session_state.work_days:
            st.session_state.work_days.append(new_work_day)
            st.session_state.results = None
            st.rerun()
        else:
            st.warning(
                "That date and location have already been added."
            )

with button_column_2:
    if st.button(
        "Clear Schedule",
        use_container_width=True,
    ):
        st.session_state.work_days = []
        st.session_state.results = None
        st.rerun()


# =============================================================================
# Display Schedule
# =============================================================================

schedule = pd.DataFrame(
    st.session_state.work_days
)

if not schedule.empty:
    schedule["Work Date"] = pd.to_datetime(
        schedule["Work Date"],
        errors="coerce",
    ).dt.date

    schedule["Work Location"] = (
        schedule["Work Location"]
        .astype("string")
        .str.strip()
    )

    schedule = schedule.drop_duplicates(
        subset=[
            "Work Date",
            "Work Location",
        ]
    )

    st.dataframe(
        schedule,
        hide_index=True,
        use_container_width=True,
    )
else:
    st.info(
        "Add at least one employee work date and location."
    )


# =============================================================================
# Step 3: Generate Report
# =============================================================================

render_section_header(
    label="Step 3",
    title="Generate Grooming Report",
)

if st.button(
    "Generate Report",
    type="primary",
    use_container_width=True,
):
    if schedule.empty:
        st.warning(
            "Please add at least one employee work date first."
        )
    else:
        # Match the employee's shift with when the appointment was created.
        results = df.merge(
            schedule,
            left_on=[
                "Booking Date",
                "Booking Location",
            ],
            right_on=[
                "Work Date",
                "Work Location",
            ],
            how="inner",
        )

        output_columns = []

        # This is the actual date of the grooming appointment.
        if appointment_date_column is not None:
            output_columns.append(appointment_date_column)

        optional_columns = [
            "First name",
            "Last name",
            "Primary number",
            "Email",
            "Pet & services",
            "Ticket comment",
            "Booking Date",
            "Booking Location",
        ]

        output_columns.extend(
            column
            for column in optional_columns
            if column in results.columns
        )

        results = results[output_columns].copy()

        rename_columns = {
            "First name": "First Name",
            "Last name": "Last Name",
            "Primary number": "Primary Number",
            "Booking Location": "Booked At Location",
        }

        if appointment_date_column is not None:
            rename_columns[appointment_date_column] = (
                "Appointment Date"
            )

        results = results.rename(
            columns=rename_columns
        )

        sort_columns = [
            column
            for column in [
                "Booking Date",
                "Appointment Date",
                "Last Name",
            ]
            if column in results.columns
        ]

        if sort_columns:
            results = results.sort_values(
                by=sort_columns,
                ignore_index=True,
            )

        st.session_state.results = results


# =============================================================================
# Results and Download
# =============================================================================

if st.session_state.results is not None:
    results = st.session_state.results

    st.success(
        f"{len(results)} appointments found."
    )

    st.dataframe(
        results,
        hide_index=True,
        use_container_width=True,
    )

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl",
    ) as writer:
        results.to_excel(
            writer,
            index=False,
            sheet_name="Grooming Appointments",
        )

    st.download_button(
        label="Download Groom Report",
        data=output.getvalue(),
        file_name="Grooming_Report.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True,
    )
import streamlit as st
import pandas as pd
from io import BytesIO

from utils.styling.base import apply_base_styles, render_hero
from utils.components.headers import render_section_header

st.set_page_config(
    page_title="Grooming Sort",
    page_icon="✂️",
    layout="wide",
)

apply_base_styles()

render_hero(
    "Grooming Appointment Sorter",
    (
        "Filter MoeGo appointment reports by employee "
        "work dates and locations."
    ),
)

render_section_header(
    label="Step 1",
    title="Upload MoeGo Report",
)

uploaded_file = st.file_uploader(
    "Upload Appointment Schedule",
    type=["csv"]
)


if uploaded_file is None:
    st.stop()

df = pd.read_csv(uploaded_file)


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
        c for c in remove_columns
        if c in df.columns
    ]
)


df = df.rename(
    columns={
        "Create by": "Created",
        "Create date": "Booked",
    }
)


df["Booked"] = pd.to_datetime(
    df["Booked"],
    errors="coerce",
).dt.date


df = df[
    df["Created"].notna()
]


df = df.drop_duplicates()
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
new_date = st.date_input(
    "Work Date"
)


location = st.selectbox(
    "Location",
    locations,
)


if st.button("Add Work Day"):

    st.session_state.work_days.append(
        {
            "Date": new_date,
            "Location": location
        }
    )
schedule = pd.DataFrame(
    st.session_state.work_days
)
if not schedule.empty:
    schedule["Date"] = pd.to_datetime(
        schedule["Date"]
    ).dt.date


if not schedule.empty:

    st.dataframe(
        schedule,
        hide_index=True,
    )

if st.button("Generate Report"):

    results = df.merge(
        schedule,
        left_on=[
            "Booked",
            "Created"
        ],
        right_on=[
            "Date",
            "Location"
        ],
        how="inner"
    )


    results = results[
        [
            "Date",
            "First name",
            "Last name",
            "Primary number",
            "Email",
            "Booked",
            "Created",
            "Ticket comment",
        ]
    ]


    st.session_state.results = results

if "results" in st.session_state:

    st.success(
        f"{len(st.session_state.results)} appointments found"
    )


    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="xlsxwriter"
    ) as writer:

        st.session_state.results.to_excel(
            writer,
            index=False,
        )


    st.download_button(
        label="Download Groom Report",
        data=output.getvalue(),
        file_name="Grooming_Report.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
    )
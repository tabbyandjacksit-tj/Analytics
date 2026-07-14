# =============================================================================
# IMPORTS
# =============================================================================

from datetime import datetime

import pandas as pd
import streamlit as st

from utils.officehours import (
    format_minutes,
    get_active_tasks,
    get_week_start,
    prepare_tasks,
)
from utils.sheet_reader import load_private_sheet
from utils.styling.base import apply_base_styles, render_hero


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Office Hour Tracker",
    page_icon="images/logo.png",
    layout="wide",
)

apply_base_styles(max_width=1160)

render_hero(
    "Office Hour Tracker",
    "See who is currently working and open any employee's weekly task tracker.",
)


# =============================================================================
# GOOGLE SHEET SETTINGS
# =============================================================================

SHEET_ID = st.secrets["OFFICE_HOURS_SHEET_ID"]
EMPLOYEES_TAB = "Employees"
TASKS_TAB = "Tasks"


# =============================================================================
# LOAD DATA
# =============================================================================

try:
    employees_df = load_private_sheet(
        SHEET_ID,
        EMPLOYEES_TAB,
    )

    tasks_df = prepare_tasks(
        load_private_sheet(
            SHEET_ID,
            TASKS_TAB,
        )
    )

except Exception as error:
    st.error(f"Could not load the Office Hours data: {error}")
    st.stop()


# =============================================================================
# PREPARE EMPLOYEE LIST
# =============================================================================

required_employee_columns = {"Employee", "Active"}

if not required_employee_columns.issubset(employees_df.columns):
    st.error(
        "The Employees sheet must contain these columns: "
        "Employee and Active."
    )
    st.stop()

active_values = {
    "true",
    "yes",
    "1",
    "active",
}

employees = (
    employees_df.loc[
        employees_df["Active"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(active_values),
        "Employee",
    ]
    .fillna("")
    .astype(str)
    .str.strip()
)

employees = sorted(
    employee
    for employee in employees.unique()
    if employee
)

if not employees:
    st.warning("No active employees were found in the Employees sheet.")


# =============================================================================
# WHO'S WORKING NOW
# =============================================================================

st.markdown("## Who's Working Now?")

active_tasks = get_active_tasks(tasks_df)

if active_tasks.empty:
    st.info("Nobody is currently tracking an active office-hour task.")

else:
    active_tasks = active_tasks.sort_values(
        "Start Time",
        ascending=True,
    )

    for row_start in range(0, len(active_tasks), 3):
        columns = st.columns(3, gap="large")

        visible_tasks = active_tasks.iloc[row_start:row_start + 3]

        for column, (_, task) in zip(
            columns,
            visible_tasks.iterrows(),
        ):
            started_at = pd.to_datetime(
                task["Start Time"],
                errors="coerce",
            )

            if pd.notna(started_at):
                elapsed_minutes = (
                    datetime.now() - started_at.to_pydatetime()
                ).total_seconds() / 60

                started_label = (
                    started_at
                    .to_pydatetime()
                    .strftime("%I:%M %p")
                    .lstrip("0")
                )

                elapsed_label = format_minutes(elapsed_minutes)

            else:
                started_label = "Unknown"
                elapsed_label = "Unknown"

            with column:
                st.markdown(
                    f"""
<div style="
    background:#FFF9EF;
    border:1px solid #D7C8A4;
    border-radius:20px;
    padding:20px;
    min-height:190px;
    box-shadow:0 4px 14px rgba(47,55,45,0.07);
">
    <div style="
        color:#1D5A3E;
        font-size:20px;
        font-weight:800;
        margin-bottom:8px;
    ">
        🟢 {task["Employee"]}
    </div>

    <div style="
        color:#C97822;
        font-size:13px;
        font-weight:800;
        text-transform:uppercase;
        margin-bottom:6px;
    ">
        {task["Project"]}
    </div>

    <div style="
        color:#2F372D;
        font-size:16px;
        font-weight:700;
        margin-bottom:14px;
    ">
        {task["Task"]}
    </div>

    <div style="
        color:#5C7A58;
        font-size:14px;
        line-height:1.6;
    ">
        Started: {started_label}<br>
        Elapsed: {elapsed_label}
    </div>
</div>
""",
                    unsafe_allow_html=True,
                )


# =============================================================================
# EMPLOYEE TRACKERS
# =============================================================================

st.markdown("## Office Hour Employees")

current_week = get_week_start()

for row_start in range(0, len(employees), 3):
    columns = st.columns(3, gap="large")

    for column, employee in zip(
        columns,
        employees[row_start:row_start + 3],
    ):
        employee_week_tasks = tasks_df[
            tasks_df["Employee"].eq(employee)
            & tasks_df["Week Start"].eq(current_week.isoformat())
        ]

        completed_tasks = int(
            employee_week_tasks["Status"]
            .eq("Finished")
            .sum()
        )

        active_count = int(
            employee_week_tasks["Status"]
            .eq("Active")
            .sum()
        )

        total_minutes = pd.to_numeric(
            employee_week_tasks["Minutes"],
            errors="coerce",
        ).fillna(0).sum()

        status_label = (
            "🟢 Working Now"
            if active_count
            else "⚪ Not Active"
        )

        with column:
            st.markdown(
                f"""
<div style="
    background:#FFFDF8;
    border:1px solid #D7C8A4;
    border-radius:20px 20px 0 0;
    padding:24px;
    min-height:180px;
    box-shadow:0 5px 16px rgba(47,55,45,0.07);
">
    <div style="
        color:#1D5A3E;
        font-size:23px;
        font-weight:800;
        margin-bottom:8px;
    ">
        👤 {employee}
    </div>

    <div style="
        color:#5C7A58;
        font-size:14px;
        line-height:1.7;
    ">
        {status_label}<br>
        {completed_tasks} completed tasks this week<br>
        {format_minutes(total_minutes)} recorded this week
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

            employee_key = (
                employee.lower()
                .replace(" ", "_")
                .replace("'", "")
            )

            if st.button(
                f"Open {employee}'s Tracker →",
                key=f"open_employee_{employee_key}",
                use_container_width=True,
            ):
                st.session_state["selected_office_employee"] = employee
                st.switch_page("pages/employeetasks.py")
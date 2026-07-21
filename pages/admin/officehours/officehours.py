# =============================================================================
# Imports
# =============================================================================
from datetime import datetime
import pandas as pd
import streamlit as st
from utils.reporting.officehours import (
    format_minutes,
    get_active_tasks,
    get_week_start,
    prepare_tasks,
    LOCAL_TIMEZONE
)
from utils.tools.sheet_reader import load_private_sheet
from utils.styling.base import apply_base_styles, render_hero
from utils.styling.officehours import (
    apply_officehour_styles,
    render_active_employee,
    render_employee_card,
    render_no_active_workers,
    section_header,
)
from utils.tools.secrets import get_secret
# =======================================================================================
# Page Configuration (sets title, icon, and layout of page)
# CSS Styles also imported/applied
# =======================================================================================
SHEET_ID = get_secret("OFFICE_HOURS_SHEET_ID")
st.set_page_config(
    page_title="Office Hour Tracker",
    page_icon="images/logo.png",
    layout="wide",
)
apply_base_styles(max_width=1160)
apply_officehour_styles()
render_hero(
    "Office Hour Tracker",
    "See who is currently working and open any employee's weekly task tracker.",
)
# =============================================================================
# Google sheet settings & also loading in the sheet using functions from helpers.
# =============================================================================
EMPLOYEES_TAB = "Employees"
TASKS_TAB = "Tasks"
try:
    employees_df = load_private_sheet(SHEET_ID, EMPLOYEES_TAB,)
    tasks_df = prepare_tasks(
        load_private_sheet(SHEET_ID, TASKS_TAB,)
    )
except Exception as error:
    st.error(f"Could not load the Office Hours data: {error}")
    st.stop()
# =============================================================================
# Read in employee dataframe, make sure that it has employee and active! 
# =============================================================================
required_employee_columns = {
    "Employee",
    "Active",
}
if not required_employee_columns.issubset(employees_df.columns):
    st.error(
        "The Employees sheet must contain these columns: "
        "Employee and Active."
    )
    st.stop()
active_values = { # all of the possible considerations for what active might be! 
    "true",
    "yes",
    "1",
    "active",
}
employees_df["Employee"] = (
    employees_df["Employee"]
    .fillna("")
    .astype(str)
    .map(str.strip)
)
employees_df["Active"] = (
    employees_df["Active"]
    .fillna("")
    .astype(str)
    .map(str.strip)
    .map(str.lower)
)
employees = sorted(
    employees_df.loc[
        employees_df["Active"].isin(active_values),
        "Employee",
    ]
    .loc[lambda values: values.ne("")]
    .unique()
)
if not employees:
    st.warning("There are currently no active employees!")
# =============================================================================
# Creates the section for "Who is Working Now?"
# =============================================================================
section_header("Who's Working Now?")
active_tasks = get_active_tasks(tasks_df) # Obtains the task that is active in the tasks_df that is defined! 
if active_tasks.empty:
    render_no_active_workers()
else:
    active_tasks = active_tasks.sort_values("Start Time", ascending = True,)# Sorts in order of when they were done 
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
                started_datetime = started_at.to_pydatetime()
                if started_datetime.tzinfo is None:
                    started_datetime = started_datetime.replace(tzinfo=LOCAL_TIMEZONE)
                elapsed_minutes = (datetime.now(LOCAL_TIMEZONE) - started_datetime).total_seconds() / 60
                started_label = (
                    started_at
                    .to_pydatetime()
                    .strftime("%I:%M %p")
                    .lstrip("0")
                )
                elapsed_label = format_minutes(
                    elapsed_minutes
                )
            else:
                started_label = "Unknown"
                elapsed_label = "Unknown"
            with column:
                render_active_employee(
                    employee=task["Employee"],
                    project=task["Project"],
                    task= "",
                    clock_in=started_label,
                    elapsed=elapsed_label,
                )
# =============================================================================
# Creates the cards for each employees weekly tasks 
# =============================================================================
section_header(
    "Office Hour Employees",
    "Open any employee's tracker to view and manage weekly tasks.",
)
current_week = get_week_start()
for row_start in range(0, len(employees), 3):
    columns = st.columns(3, gap="large")
    for column, employee in zip(
        columns,
        employees[row_start:row_start + 3],
    ):
        employee_week_tasks = tasks_df[
            tasks_df["Employee"].eq(employee)
            & tasks_df["Week Start"].eq(
                current_week.isoformat()
            )
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
        total_minutes = pd.to_numeric(employee_week_tasks["Minutes"], errors="coerce",).fillna(0).sum()
        employee_key = (
            employee.lower()
            .replace(" ", "_")
            .replace("'", "")
        )
        with column:
            render_employee_card(
                employee=employee,
                completed_tasks=completed_tasks,
                total_minutes=format_minutes(total_minutes),
                active=bool(active_count),
            )
            if st.button(
                f"Open {employee}'s Tracker →",
                key=f"open_employee_{employee_key}",
                use_container_width=True,
            ):
                st.session_state["selected_office_employee"] = employee
                st.switch_page(
                    "pages/admin/officehours/employeetasks.py"
                )
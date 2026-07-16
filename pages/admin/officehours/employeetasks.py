# =============================================================================
# IMPORTS
# =============================================================================

from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from utils.reporting.officehours import (
    TASK_COLUMNS,
    create_task_record,
    finish_task_record,
    format_minutes,
    get_employee_tasks,
    get_week_start,
    prepare_tasks,
    start_task_record,
)
from utils.tools.sheet_reader import (
    append_row,
    load_private_sheet,
    update_row_by_id,
)
from utils.styling.base import apply_base_styles, render_hero
from utils.styling.officehours import (
    apply_officehour_styles,
    render_active_task,
    render_no_active_task,
    render_task_card,
    section_header,
)

from utils.tools.secrets import get_secret

SHEET_ID = get_secret("OFFICE_HOURS_SHEET_ID")


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Employee Office Hours",
    page_icon="images/logo.png",
    layout="wide",
)

apply_base_styles(max_width=1100)
apply_officehour_styles()


# =============================================================================
# GOOGLE SHEET SETTINGS
# =============================================================================

TASKS_TAB = "Tasks"


# =============================================================================
# EMPLOYEE SELECTION
# =============================================================================

employee = st.session_state.get("selected_office_employee")

if not employee:
    st.warning("Please choose an employee first.")

    if st.button(
        "← Return to Office Hours",
        use_container_width=True,
    ):
        st.switch_page("pages/officehours.py")

    st.stop()


# =============================================================================
# WEEK SELECTION
# =============================================================================

current_week = get_week_start()

week_options = [
    current_week,
    current_week - timedelta(weeks=1),
    current_week - timedelta(weeks=2),
    current_week - timedelta(weeks=3),
    current_week - timedelta(weeks=4),
]

selected_week = st.selectbox(
    "Select Week",
    options=week_options,
    format_func=lambda week_start: (
        f"Week of {week_start.strftime('%B %d, %Y')}"
    ),
)

week_end = selected_week + timedelta(days=6)


# =============================================================================
# PAGE HEADER
# =============================================================================

render_hero(
    f"{employee}'s Office Hours",
    (
        f"Tasks for {selected_week.strftime('%B %d')} through "
        f"{week_end.strftime('%B %d, %Y')}."
    ),
)


# =============================================================================
# LOAD TASKS
# =============================================================================

try:
    tasks_df = prepare_tasks(
        load_private_sheet(
            SHEET_ID,
            TASKS_TAB,
        )
    )

except Exception as error:
    st.error(f"Could not load office-hour tasks: {error}")
    st.stop()

employee_tasks = get_employee_tasks(
    tasks_df,
    employee,
    selected_week,
)


# =============================================================================
# WEEKLY SUMMARY
# =============================================================================

todo_count = int(
    employee_tasks["Status"].eq("To Do").sum()
)

active_count = int(
    employee_tasks["Status"].eq("Active").sum()
)

finished_count = int(
    employee_tasks["Status"].eq("Finished").sum()
)

total_minutes = pd.to_numeric(
    employee_tasks["Minutes"],
    errors="coerce",
).fillna(0).sum()

summary_1, summary_2, summary_3, summary_4 = st.columns(4)

summary_1.metric("To Do", todo_count)
summary_2.metric("Active", active_count)
summary_3.metric("Finished", finished_count)
summary_4.metric(
    "Tracked Time",
    format_minutes(total_minutes),
)


# =============================================================================
# ADD TASK
# =============================================================================

section_header(
    "Add New Task",
    "Create a task for the current week before starting the timer.",
)

with st.form(
    "new_task",
    clear_on_submit=True,
):
    project = st.text_input(
        "Project",
        placeholder="Example: Analytics Hub",
    )

    task_description = st.text_input(
        "Task",
        placeholder="Describe what needs to be completed.",
    )

    notes = st.text_area(
        "Notes",
        placeholder="Optional context or next steps.",
        height=90,
    )

    submitted = st.form_submit_button(
        "Add Task",
        use_container_width=True,
    )

if submitted:
    if selected_week != current_week:
        st.error("New tasks can only be added to the current week.")

    elif not project.strip():
        st.error("Enter a project name.")

    elif not task_description.strip():
        st.error("Enter a task description.")

    else:
        new_task = create_task_record(
            employee=employee,
            project=project,
            task=task_description,
            notes=notes,
        )

        try:
            append_row(
                SHEET_ID,
                TASKS_TAB,
                new_task,
                TASK_COLUMNS,
            )

            st.cache_data.clear()
            st.success("Task added.")
            st.rerun()

        except Exception as error:
            st.error(f"Could not add the task: {error}")


# =============================================================================
# ACTIVE TASK
# =============================================================================

section_header(
    "Currently Working",
    "Only one task can be active at a time.",
)

active_tasks = employee_tasks[
    employee_tasks["Status"].eq("Active")
].copy()

if active_tasks.empty:
    render_no_active_task()

else:
    for _, active_task in active_tasks.iterrows():
        started_at = pd.to_datetime(
            active_task["Start Time"],
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

        render_active_task(
            project=active_task["Project"],
            task=active_task["Task"],
            started=started_label,
            elapsed=elapsed_label,
            notes=active_task["Notes"],
        )

        if st.button(
            "Stop and Mark Finished",
            key=f"finish_{active_task['Task ID']}",
            use_container_width=True,
        ):
            finished_task = finish_task_record(
                active_task.to_dict()
            )

            try:
                updated = update_row_by_id(
                    SHEET_ID,
                    TASKS_TAB,
                    active_task["Task ID"],
                    finished_task,
                    TASK_COLUMNS,
                )

                if updated:
                    st.cache_data.clear()
                    st.success("Task marked as finished.")
                    st.rerun()
                else:
                    st.error(
                        "The task could not be found in the Google Sheet."
                    )

            except Exception as error:
                st.error(f"Could not finish the task: {error}")


# =============================================================================
# TO-DO TASKS
# =============================================================================

section_header(
    "To Do",
    "Start a task to begin tracking time.",
)

todo_tasks = employee_tasks[
    employee_tasks["Status"].eq("To Do")
].copy()

if todo_tasks.empty:
    st.caption("No tasks are waiting to be started.")

else:
    for _, todo_task in todo_tasks.iterrows():
        task_column, button_column = st.columns([5, 1])

        with task_column:
            render_task_card(
                project=todo_task["Project"],
                task=todo_task["Task"],
                notes=todo_task["Notes"],
            )

        with button_column:
            start_disabled = (
                not active_tasks.empty
                or selected_week != current_week
            )

            if st.button(
                "Start",
                key=f"start_{todo_task['Task ID']}",
                use_container_width=True,
                disabled=start_disabled,
            ):
                started_task = start_task_record(
                    todo_task.to_dict()
                )

                try:
                    updated = update_row_by_id(
                        SHEET_ID,
                        TASKS_TAB,
                        todo_task["Task ID"],
                        started_task,
                        TASK_COLUMNS,
                    )

                    if updated:
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(
                            "The task could not be found in the Google Sheet."
                        )

                except Exception as error:
                    st.error(f"Could not start the task: {error}")

    if not active_tasks.empty:
        st.caption(
            "Finish the current task before starting another."
        )


# =============================================================================
# FINISHED TASKS
# =============================================================================

section_header(
    "Finished",
    "Completed tasks for the selected week.",
)

finished_tasks = employee_tasks[
    employee_tasks["Status"].eq("Finished")
].copy()

if finished_tasks.empty:
    st.caption("No tasks have been finished this week.")

else:
    finished_tasks["Completed Date"] = pd.to_datetime(
        finished_tasks["Completed Date"],
        errors="coerce",
    )

    finished_tasks = finished_tasks.sort_values(
        "Completed Date",
        ascending=False,
    )

    finished_tasks["Completed Date"] = (
        finished_tasks["Completed Date"]
        .dt.strftime("%B %d, %Y")
        .fillna("")
    )

    finished_display = finished_tasks[
        [
            "Completed Date",
            "Project",
            "Task",
            "Minutes",
            "Notes",
        ]
    ].copy()

    st.dataframe(
        finished_display,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Minutes": st.column_config.NumberColumn(
                "Minutes",
                format="%.1f min",
            ),
        },
    )


# =============================================================================
# RETURN TO OFFICE HOURS
# =============================================================================

st.divider()

if st.button(
    "← Return to Office Hours",
    use_container_width=True,
):
    st.switch_page("pages/officehours.py")
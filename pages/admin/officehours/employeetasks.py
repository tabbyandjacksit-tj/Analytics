# =============================================================================
# IMPORTS
# =============================================================================
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pandas as pd
import streamlit as st
from utils.reporting.officehours import (
    LOCAL_TIMEZONE,
    TASK_COLUMNS,
    create_task_record,
    finish_task_record,
    format_minutes,
    get_employee_tasks,
    get_week_start,
    pause_task_record,
    prepare_tasks,
    resume_task_record,
    start_task_record,
)
from utils.tools.sheet_reader import (
    append_row,
    load_private_sheet,
    update_row_by_id,
)
from utils.styling.officehours import (
    apply_officehour_styles,
    render_active_task,
    render_no_active_task,
    render_task_card,
)
from utils.styling.base import (
    apply_base_styles,
    render_hero,
)
from utils.components.headers import (
    render_section_header,
    render_subsection_header,
)
from utils.styling.components import apply_component_styles
from utils.tools.secrets import get_secret
SHEET_ID = get_secret("OFFICE_HOURS_SHEET_ID")
LOCAL_TIMEZONE = ZoneInfo("America/Chicago") # Sets the time zone so that the record tracks correctly. 
# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Employee Office Hours",
    page_icon="images/logo.png",
    layout="wide",
)
apply_base_styles(max_width=1100)
apply_component_styles()
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
        st.switch_page("pages/admin/officehours/officehours.py")

    st.stop()

# =============================================================================
# Creates a place for the employees to get_week_start and also have a selection for previous weeks 
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
week_end = selected_week + timedelta(days=6) # Sets the end of the week 6 days out because 7 overlaps with starting than! 
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
        load_private_sheet(SHEET_ID, TASKS_TAB,))
except Exception as error:
    st.error(f"Could not load office-hour tasks: {error}")
    st.stop()
employee_tasks = get_employee_tasks( # Runs get_employee_tasks  to obtain tasks_df, employee, selected_week.
    tasks_df,
    employee,
    selected_week,
)
# =============================================================================
# Creates the weekly tracker of what is left to do, what is in progress, what is finished, etc. 
# =============================================================================
todo_count = int(employee_tasks["Status"].eq("To Do").sum())
active_count = int(employee_tasks["Status"].eq("Active").sum())
in_progress_count = int(employee_tasks["Status"].eq("In Progress").sum())
finished_count = int(employee_tasks["Status"].eq("Finished").sum())
total_minutes = pd.to_numeric(employee_tasks["Minutes"], errors="coerce",).fillna(0).sum()
 # Creates a summary of all 5 things above and than col's it 
summary_1, summary_2, summary_3, summary_4, summary_5 = st.columns(5) 
# Creates the metric and title for each count created above
summary_1.metric("To Do", todo_count)
summary_2.metric("Working", active_count)
summary_3.metric("In Progress", in_progress_count)
summary_4.metric("Finished", finished_count)
summary_5.metric("Tracked Time", format_minutes(total_minutes),)
# =============================================================================
# Where the adding new project form lives.
# =============================================================================
render_section_header(
    label="Project Setup",
    title="Add New Project",
    subtitle=(
        "Add a project for the selected week and include any "
        "notes or next steps."
    ),
)
with st.form(
    "new_project",
    clear_on_submit=True,
):
    project = st.text_input("Project", placeholder="Example: Balancing Sun Prairie Burlo",) 
    notes = st.text_area("Notes", placeholder="Optional description, updates, or next steps.", height=90,)
    submitted = st.form_submit_button("Add Project", use_container_width=True,)

if submitted:
    if selected_week != current_week: # Exception
        st.error("New projects can only be added to the current week.")
    elif not project.strip(): # Exception: A project name needs to be added
        st.error("Enter a project name.")
    else: 
        new_task = create_task_record( # Creates the new task based on the inputed info defined above
            employee=employee,
            project=project.strip(),
            task="",
            notes=notes.strip(),
        )
        try:
            append_row(
                SHEET_ID,
                TASKS_TAB,
                new_task,
                TASK_COLUMNS,
            )
            st.cache_data.clear()
            st.success("Project added.")
            st.rerun()
        except Exception as error:
            st.error(f"Could not add the project: {error}")
# =============================================================================
# Creates the section for the projects that are currently being worked on
# =============================================================================

render_section_header(
    label="Active Project",
    title="Currently Working",
    subtitle="Only one project can be actively timed at a time.",
)

active_tasks = employee_tasks[employee_tasks["Status"].eq("Active")].copy()

if active_tasks.empty:
    render_no_active_task()
else:
    for _, active_task in active_tasks.iterrows():
        started_at = pd.to_datetime(active_task["Start Time"], errors="coerce",)
        if pd.notna(started_at):
            started_datetime = started_at.to_pydatetime()
            if started_datetime.tzinfo is None:
                started_datetime = started_datetime.replace(
                    tzinfo=LOCAL_TIMEZONE
                )
            elapsed_minutes = (
                datetime.now(LOCAL_TIMEZONE)
                - started_datetime
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
            task="",
            started=started_label,
            elapsed=elapsed_label,
            notes=active_task["Notes"],
        )
        pause_column, finish_column = st.columns(2)
        with pause_column:
            pause_clicked = st.button(
                "Pause",
                key=f"pause_{active_task['Task ID']}",
                use_container_width=True,
                disabled=selected_week != current_week,
            )
        with finish_column:
            finish_clicked = st.button(
                "Mark Finished",
                key=f"finish_{active_task['Task ID']}",
                use_container_width=True,
                disabled=selected_week != current_week,
            )
        if pause_clicked:
            paused_task = pause_task_record(
                active_task.to_dict()
            )
            try:
                updated = update_row_by_id(
                    SHEET_ID,
                    TASKS_TAB,
                    active_task["Task ID"],
                    paused_task,
                    TASK_COLUMNS,
                )
                if updated:
                    st.cache_data.clear()
                    st.success("Project paused.")
                    st.rerun()
                else:
                    st.error(
                        "The project could not be found "
                        "in the Google Sheet."
                    )
            except Exception as error: # Catches any exception as an error 
                st.error(
                    f"Could not pause the project: {error}"
                )
        if finish_clicked:
            finished_task = finish_task_record(active_task.to_dict())
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
                    st.success(
                        "Project marked as finished."
                    )
                    st.rerun()
                else:
                    st.error(
                        "The project could not be found "
                        "in the Google Sheet."
                    )
            except Exception as error:
                st.error(
                    f"Could not finish the project: {error}"
                )
# =============================================================================
# Tracks and creates a section for projects that are in progress 
# =============================================================================
render_subsection_header(
    title="In Progress",
    subtitle="Paused projects that can be resumed.",
)
in_progress_tasks = employee_tasks[employee_tasks["Status"].eq("In Progress")].copy()
if in_progress_tasks.empty:
    st.caption("No projects are currently paused.")
else:
    for _, progress_task in in_progress_tasks.iterrows():
        project_column, button_column = st.columns([5, 1])
        with project_column:
            render_task_card(
                project=progress_task["Project"],
                task="",
                notes=progress_task["Notes"],
            )

        with button_column:
            resume_disabled = (
                not active_tasks.empty
                or selected_week != current_week
            )

            if st.button(
                "Resume",
                key=f"resume_{progress_task['Task ID']}",
                use_container_width=True,
                disabled=resume_disabled,
            ):
                resumed_task = resume_task_record(
                    progress_task.to_dict()
                )

                try:
                    updated = update_row_by_id(
                        SHEET_ID,
                        TASKS_TAB,
                        progress_task["Task ID"],
                        resumed_task,
                        TASK_COLUMNS,
                    )

                    if updated:
                        st.cache_data.clear()
                        st.success("Project resumed.")
                        st.rerun()

                    else:
                        st.error(
                            "The project could not be found "
                            "in the Google Sheet."
                        )

                except Exception as error:
                    st.error(
                        f"Could not resume the project: {error}"
                    )
    if not active_tasks.empty:
        st.caption(
            "Pause or finish the current project before "
            "resuming another."
        )
# =============================================================================
# Creates the section for the tasks that are marked as needed to be done 
# =============================================================================
render_subsection_header(
    title="To Do",
    subtitle="Projects that have not been started.",
)
todo_tasks = employee_tasks[employee_tasks["Status"].eq("To Do")].copy()
if todo_tasks.empty:
    st.caption("No projects are waiting to be started.")
else:
    for _, todo_task in todo_tasks.iterrows():
        task_column, button_column = st.columns([5, 1])
        with task_column:
            render_task_card(
                project=todo_task["Project"],
                task= "",
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
        st.caption( # You must be only current on one task. 
            "Finish the current task before starting another."
        )
# =============================================================================
# Holds all of the finished tasks and outputs a report. These are also copied down
# to the office tracker sheet that is established with the GID above, or through
# tabbyandjacksIT@gmail.com
# =============================================================================
render_subsection_header(
    title="Finished",
    subtitle="Projects completed during the selected week.",
)
finished_tasks = employee_tasks[employee_tasks["Status"].eq("Finished")].copy()
if finished_tasks.empty:
    st.caption("No tasks have been finished this week.")
else:
    finished_tasks["Completed Date"] = pd.to_datetime(finished_tasks["Completed Date"],errors="coerce",)
    finished_tasks = finished_tasks.sort_values("Completed Date", ascending=False,)
    finished_tasks["Completed Date"] = (
        finished_tasks["Completed Date"]
        .dt.strftime("%B %d, %Y")
        .fillna("")
    )
    finished_display = finished_tasks[
        [
            "Completed Date",
            "Project",
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
# Lets you switch the page around again 
# ============================================================================
st.divider()
if st.button(
    "← Return to Office Hours",
    use_container_width=True,
):
    st.switch_page("pages/admin/officehours/officehours.py")
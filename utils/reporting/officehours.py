# =============================================================================
# IMPORTS
# =============================================================================

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from uuid import uuid4

import pandas as pd


# =============================================================================
# GOOGLE SHEET COLUMNS
# =============================================================================

TASK_COLUMNS = [
    "Task ID",
    "Employee",
    "Week Start",
    "Created Date",
    "Project",
    "Task",
    "Status",
    "Start Time",
    "End Time",
    "Minutes",
    "Completed Date",
    "Notes",
]

LOCAL_TIMEZONE = ZoneInfo("America/Chicago")


# =============================================================================
# DATE HELPERS
# =============================================================================

def get_week_start(target_date: date | None = None) -> date:
    """Return the Monday for the supplied date."""
    target_date = target_date or date.today()

    return target_date - timedelta(
        days=target_date.weekday()
    )


# =============================================================================
# TIME HELPERS
# =============================================================================

def get_saved_minutes(task: dict) -> float:
    """Return previously recorded minutes as a number."""
    minutes = pd.to_numeric(
        task.get("Minutes", 0),
        errors="coerce",
    )

    if pd.isna(minutes):
        return 0.0

    return float(minutes)


def get_active_session_minutes(task: dict) -> float:
    """Return minutes elapsed during the current active session."""
    started_at = pd.to_datetime(
        task.get("Start Time", ""),
        errors="coerce",
    )

    if pd.isna(started_at):
        return 0.0

    elapsed_minutes = (
        datetime.now(LOCAL_TIMEZONE)
        - started_at.to_pydatetime()
    ).total_seconds() / 60

    return max(elapsed_minutes, 0.0)


# =============================================================================
# CREATE PROJECT
# =============================================================================

def create_task_record(
    employee: str,
    project: str,
    task: str = "",
    notes: str = "",
) -> dict:
    """Create a new project record in To Do status."""
    today = date.today()

    return {
        "Task ID": str(uuid4()),
        "Employee": employee.strip(),
        "Week Start": get_week_start(today).isoformat(),
        "Created Date": today.isoformat(),
        "Project": project.strip(),
        "Task": task.strip(),
        "Status": "To Do",
        "Start Time": "",
        "End Time": "",
        "Minutes": 0,
        "Completed Date": "",
        "Notes": notes.strip(),
    }


# =============================================================================
# START PROJECT
# =============================================================================

def start_task_record(task: dict) -> dict:
    """Start a To Do project without removing saved time."""
    updated_task = task.copy()

    updated_task["Status"] = "Active"
    updated_task["Start Time"] = datetime.now(LOCAL_TIMEZONE).isoformat(
        timespec="seconds"
    )
    updated_task["End Time"] = ""
    updated_task["Completed Date"] = ""

    if not str(
        updated_task.get("Minutes", "")
    ).strip():
        updated_task["Minutes"] = 0

    return updated_task


# =============================================================================
# PAUSE PROJECT
# =============================================================================

def pause_task_record(task: dict) -> dict:
    """Pause an active project and preserve tracked time."""
    updated_task = task.copy()

    saved_minutes = get_saved_minutes(
        updated_task
    )

    active_minutes = get_active_session_minutes(
        updated_task
    )

    updated_task["Status"] = "In Progress"
    updated_task["Minutes"] = round(
        saved_minutes + active_minutes,
        1,
    )
    updated_task["Start Time"] = ""
    updated_task["End Time"] = ""
    updated_task["Completed Date"] = ""

    return updated_task


# =============================================================================
# RESUME PROJECT
# =============================================================================

def resume_task_record(task: dict) -> dict:
    """Resume an In Progress project without clearing saved time."""
    updated_task = task.copy()

    updated_task["Status"] = "Active"
    updated_task["Start Time"] = datetime.now(LOCAL_TIMEZONE).isoformat(
        timespec="seconds"
    )
    updated_task["End Time"] = ""
    updated_task["Completed Date"] = ""

    return updated_task


# =============================================================================
# FINISH PROJECT
# =============================================================================

def finish_task_record(task: dict) -> dict:
    """Finish a project while preserving all tracked time."""
    updated_task = task.copy()
    finished_at = datetime.now(LOCAL_TIMEZONE)

    saved_minutes = get_saved_minutes(
        updated_task
    )

    active_minutes = 0.0

    if updated_task.get("Status") == "Active":
        active_minutes = get_active_session_minutes(
            updated_task
        )

    total_minutes = round(
        saved_minutes + active_minutes,
        1,
    )

    updated_task["Status"] = "Finished"
    updated_task["Start Time"] = ""
    updated_task["End Time"] = finished_at.isoformat(
        timespec="seconds"
    )
    updated_task["Minutes"] = total_minutes
    updated_task["Completed Date"] = (
        finished_at.date().isoformat()
    )

    return updated_task


# =============================================================================
# PREPARE GOOGLE SHEET DATA
# =============================================================================

def prepare_tasks(
    tasks_df: pd.DataFrame,
) -> pd.DataFrame:
    """Normalize project data loaded from Google Sheets."""
    tasks_df = tasks_df.copy()

    for column in TASK_COLUMNS:
        if column not in tasks_df.columns:
            tasks_df[column] = ""

    tasks_df = tasks_df[TASK_COLUMNS]
    tasks_df = tasks_df.fillna("")

    text_columns = [
        "Task ID",
        "Employee",
        "Week Start",
        "Created Date",
        "Project",
        "Task",
        "Status",
        "Start Time",
        "End Time",
        "Completed Date",
        "Notes",
    ]

    for column in text_columns:
        tasks_df[column] = (
            tasks_df[column]
            .astype(str)
            .map(str.strip)
        )

    tasks_df["Minutes"] = pd.to_numeric(
        tasks_df["Minutes"],
        errors="coerce",
    ).fillna(0)

    return tasks_df


# =============================================================================
# FILTER EMPLOYEE PROJECTS
# =============================================================================

def get_employee_tasks(
    tasks_df: pd.DataFrame,
    employee: str,
    week_start: date,
) -> pd.DataFrame:
    """Return one employee's projects for one week."""
    return tasks_df[
        tasks_df["Employee"].eq(employee)
        & tasks_df["Week Start"].eq(
            week_start.isoformat()
        )
    ].copy()


# =============================================================================
# FILTER ACTIVE PROJECTS
# =============================================================================

def get_active_tasks(
    tasks_df: pd.DataFrame,
) -> pd.DataFrame:
    """Return every project currently being timed."""
    return tasks_df[
        tasks_df["Status"].eq("Active")
    ].copy()


# =============================================================================
# DISPLAY TIME
# =============================================================================

def format_minutes(
    minutes: float | int | str,
) -> str:
    """Format stored minutes as hours and minutes."""
    try:
        total_minutes = int(
            float(minutes)
        )

    except (TypeError, ValueError):
        return "0m"

    hours, remaining_minutes = divmod(
        total_minutes,
        60,
    )

    if hours:
        return (
            f"{hours}h "
            f"{remaining_minutes}m"
        )

    return f"{remaining_minutes}m"
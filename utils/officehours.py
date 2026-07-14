from datetime import date, datetime, timedelta
from uuid import uuid4

from utils.sheet_reader import (
    append_row,
    load_private_sheet,
    update_row_by_id,
)

import pandas as pd


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


def get_week_start(target_date: date | None = None) -> date:
    """Return the Monday for the supplied date."""
    target_date = target_date or date.today()
    return target_date - timedelta(days=target_date.weekday())


def create_task_record(
    employee: str,
    project: str,
    notes: str = "",
) -> dict:
    """Create a new task record in To Do status."""
    today = date.today()

    return {
        "Task ID": str(uuid4()),
        "Employee": employee,
        "Week Start": get_week_start(today).isoformat(),
        "Created Date": today.isoformat(),
        "Project": project.strip(),
        "Status": "To Do",
        "Start Time": "",
        "End Time": "",
        "Minutes": "",
        "Completed Date": "",
        "Notes": notes.strip(),
    }


def start_task_record(task: dict) -> dict:
    """Return a task updated to Active status."""
    updated_task = task.copy()
    updated_task["Status"] = "Active"
    updated_task["Start Time"] = datetime.now().isoformat(timespec="seconds")
    updated_task["End Time"] = ""
    updated_task["Minutes"] = ""
    updated_task["Completed Date"] = ""

    return updated_task


def finish_task_record(task: dict) -> dict:
    """Return a task updated to Finished status."""
    updated_task = task.copy()
    finished_at = datetime.now()

    started_at = pd.to_datetime(
        updated_task["Start Time"],
        errors="coerce",
    )

    minutes = 0

    if pd.notna(started_at):
        minutes = round(
            (finished_at - started_at.to_pydatetime()).total_seconds() / 60,
            1,
        )

    updated_task["Status"] = "Finished"
    updated_task["End Time"] = finished_at.isoformat(timespec="seconds")
    updated_task["Minutes"] = minutes
    updated_task["Completed Date"] = finished_at.date().isoformat()

    return updated_task


def prepare_tasks(tasks_df: pd.DataFrame) -> pd.DataFrame:
    """Normalize task data loaded from Google Sheets."""
    tasks_df = tasks_df.copy()

    for column in TASK_COLUMNS:
        if column not in tasks_df.columns:
            tasks_df[column] = ""

    tasks_df = tasks_df[TASK_COLUMNS]
    tasks_df = tasks_df.fillna("")

    return tasks_df


def get_employee_tasks(
    tasks_df: pd.DataFrame,
    employee: str,
    week_start: date,
) -> pd.DataFrame:
    """Return one employee's tasks for one week."""
    return tasks_df[
        tasks_df["Employee"].eq(employee)
        & tasks_df["Week Start"].eq(week_start.isoformat())
    ].copy()


def get_active_tasks(tasks_df: pd.DataFrame) -> pd.DataFrame:
    """Return every currently active task."""
    return tasks_df[tasks_df["Status"].eq("Active")].copy()


def format_minutes(minutes: float | int | str) -> str:
    """Format stored minutes as hours and minutes."""
    try:
        total_minutes = int(float(minutes))
    except (TypeError, ValueError):
        return "0m"

    hours, remaining_minutes = divmod(total_minutes, 60)

    if hours:
        return f"{hours}h {remaining_minutes}m"

    return f"{remaining_minutes}m"
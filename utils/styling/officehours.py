# =============================================================================
# IMPORTS
# =============================================================================

import html

import streamlit as st

from utils.styling.base import apply_extra_css


# =============================================================================
# STYLES
# =============================================================================

def apply_officehour_styles() -> None:
    apply_extra_css(
        """
.section-label {
    color: #C97822;
    font-size: 13px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
}

.section-title {
    color: #1D5A3E;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #5C7A58;
    font-size: 16px;
    margin-bottom: 20px;
}

.employee-card {
    background: #FFFDF8;
    border: 1px solid #D7C8A4;
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 6px 18px rgba(47, 55, 45, .08);
}

.employee-name {
    color: #1D5A3E;
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 10px;
}

.employee-meta {
    color: #5C7A58;
    font-size: 14px;
    line-height: 1.6;
}

.active-card {
    background: #EAF5EE;
    border: 1px solid #A8D2B2;
    border-radius: 22px;
    padding: 24px;
    box-shadow: 0 6px 16px rgba(29, 90, 62, .08);
    margin-bottom: 10px;
}

.active-name {
    color: #1D5A3E;
    font-size: 21px;
    font-weight: 800;
}

.active-project {
    color: #1D5A3E;
    font-size: 26px;
    font-weight: 800;
    line-height: 1.2;
    text-transform: none;
    margin: 0 0 16px 0;
}

.active-task {
    color: #2F372D;
    font-size: 17px;
    font-weight: 700;
    margin-top: 6px;
}

.active-meta {
    color: #2F372D;
    font-size: 15px;
    line-height: 1.8;
    margin-top: 10px;
}

.active-notes {
    color: #5C7A58;
    font-size: 14px;
    line-height: 1.5;
    border-top: 1px solid rgba(29, 90, 62, .15);
    margin-top: 16px;
    padding-top: 14px;
}

.status-active {
    color: #1D8A45;
    font-weight: 700;
}

.status-inactive {
    color: #888;
    font-weight: 700;
}

.task-card {
    background: #FFF9EF;
    border: 1px solid #D7C8A4;
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 8px;
}

.task-project {
    color: #C97822;
    font-size: 20px;
    font-weight: 800;
    line-height: 1.25;
    text-transform: none;
}

.task-title {
    color: #1D5A3E;
    font-size: 16px;
    font-weight: 700;
    margin-top: 5px;
}

.task-notes {
    color: #5C7A58;
    font-size: 14px;
    line-height: 1.5;
    margin-top: 9px;
}
"""
    )




# =============================================================================
# EMPLOYEE CARD
# =============================================================================

def render_employee_card(
    employee: str,
    completed_tasks: int,
    total_minutes: str,
    active: bool,
) -> None:
    safe_employee = html.escape(str(employee))
    safe_total_minutes = html.escape(str(total_minutes))

    status = (
        '<span class="status-active">🟢 Active</span>'
        if active
        else '<span class="status-inactive">⚪ Not Active</span>'
    )

    st.markdown(
        (
            '<div class="employee-card">'
            f'<div class="employee-name">≽ܫ≼ {safe_employee}</div>'
            '<div class="employee-meta">'
            f'{status}<br><br>'
            f'<b>{completed_tasks}</b> completed project(s) this week<br>'
            f'<b>{safe_total_minutes}</b> recorded this week'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


# =============================================================================
# ACTIVE EMPLOYEE CARD
# =============================================================================

def render_active_employee(
    employee: str,
    project: str,
    task: str,
    clock_in: str,
    elapsed: str,
) -> None:
    safe_employee = html.escape(str(employee))
    safe_project = html.escape(str(project))
    safe_task = html.escape(str(task))
    safe_clock_in = html.escape(str(clock_in))
    safe_elapsed = html.escape(str(elapsed))

    task_html = (
        f'<div class="active-task">{safe_task}</div>'
        if safe_task
        else ""
    )

    st.markdown(
        (
            '<div class="active-card">'
            f'<div class="active-name">🟢 {safe_employee}</div>'
            f'<div class="active-project">{safe_project}</div>'
            f'{task_html}'
            '<div class="active-meta">'
            f'<b>Clocked in:</b> {safe_clock_in}<br>'
            f'<b>Elapsed:</b> {safe_elapsed}'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


# =============================================================================
# EMPTY ACTIVE EMPLOYEE STATE
# =============================================================================

def render_no_active_workers() -> None:
    st.info(
        "Nobody is currently tracking an active office-hour project."
    )


# =============================================================================
# ACTIVE PROJECT CARD
# =============================================================================

def render_active_task(
    project: str,
    task: str,
    started: str,
    elapsed: str,
    notes: str = "",
) -> None:
    """Render the currently active project card."""
    safe_project = html.escape(str(project))
    safe_task = html.escape(str(task))
    safe_started = html.escape(str(started))
    safe_elapsed = html.escape(str(elapsed))
    safe_notes = html.escape(str(notes))

    task_html = (
        f'<div class="active-task">{safe_task}</div>'
        if safe_task
        else ""
    )

    notes_html = (
        (
            '<div class="active-notes">'
            f'<b>Notes:</b> {safe_notes}'
            '</div>'
        )
        if safe_notes
        else ""
    )

    st.markdown(
        (
            '<div class="active-card">'
            f'<div class="active-project">{safe_project}</div>'
            f'{task_html}'
            '<div class="active-meta">'
            f'<b>Started:</b> {safe_started}<br>'
            f'<b>Elapsed:</b> {safe_elapsed}'
            '</div>'
            f'{notes_html}'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


# =============================================================================
# EMPTY ACTIVE PROJECT STATE
# =============================================================================

def render_no_active_task() -> None:
    """Display a message when the employee has no active project."""
    st.info("No project is currently active.")


# =============================================================================
# PROJECT CARD
# =============================================================================

def render_task_card(
    project: str,
    task: str = "",
    notes: str = "",
) -> None:
    """Render a project waiting to be started or resumed."""
    safe_project = html.escape(str(project))
    safe_task = html.escape(str(task))
    safe_notes = html.escape(str(notes))

    task_html = (
        f'<div class="task-title">{safe_task}</div>'
        if safe_task
        else ""
    )

    notes_html = (
        f'<div class="task-notes">{safe_notes}</div>'
        if safe_notes
        else ""
    )

    st.markdown(
        (
            '<div class="task-card">'
            f'<div class="task-project">{safe_project}</div>'
            f'{task_html}'
            f'{notes_html}'
            '</div>'
        ),
        unsafe_allow_html=True,
    )
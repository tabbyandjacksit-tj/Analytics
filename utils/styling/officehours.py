import streamlit as st

from utils.styling.base import apply_extra_css


# =============================================================================
# Styles
# =============================================================================

def apply_officehour_styles() -> None:
    apply_extra_css(
        """
.section-label{
    color:#C97822;
    font-size:13px;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:1px;
    margin-bottom:4px;
}

.section-title{
    color:#1D5A3E;
    font-size:32px;
    font-weight:800;
    margin-bottom:4px;
}

.section-subtitle{
    color:#5C7A58;
    font-size:16px;
    margin-bottom:20px;
}

.employee-card{
    background:#FFFDF8;
    border:1px solid #D7C8A4;
    border-radius:22px;
    padding:22px;
    box-shadow:0px 6px 18px rgba(47,55,45,.08);
}

.employee-name{
    color:#1D5A3E;
    font-size:22px;
    font-weight:800;
    margin-bottom:10px;
}

.employee-meta{
    color:#5C7A58;
    font-size:14px;
    line-height:1.6;
}

.active-card{
    background:#EAF5EE;
    border:1px solid #A8D2B2;
    border-radius:22px;
    padding:20px;
    box-shadow:0px 6px 16px rgba(29,90,62,.08);
}

.active-name{
    color:#1D5A3E;
    font-size:21px;
    font-weight:800;
}

.active-project{
    color:#C97822;
    font-size:13px;
    font-weight:800;
    text-transform:uppercase;
    margin-top:8px;
}

.active-task{
    color:#2F372D;
    font-size:16px;
    font-weight:700;
    margin-top:6px;
}

.active-meta{
    color:#5C7A58;
    font-size:14px;
    margin-top:14px;
}

.status-active{
    color:#1D8A45;
    font-weight:700;
}

.status-inactive{
    color:#888;
    font-weight:700;
}

.task-card {
    background: #FFF9EF;
    border: 1px solid #D7C8A4;
    border-radius: 16px;
    padding: 16px 18px;
    margin-bottom: 8px;
}

.task-project {
    color: #C97822;
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
}

.task-title {
    color: #1D5A3E;
    font-size: 17px;
    font-weight: 750;
    margin-top: 4px;
}

.task-notes {
    color: #5C7A58;
    font-size: 13px;
    margin-top: 7px;
}
"""
    )


# =============================================================================
# Section Header
# =============================================================================

def section_header(
    title: str,
    subtitle: str = "",
) -> None:

    st.markdown(
        f"""
<div class="section-title">{title}</div>
<div class="section-subtitle">{subtitle}</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# Employee Card
# =============================================================================

def render_employee_card(
    employee: str,
    completed_tasks: int,
    total_minutes: str,
    active: bool,
) -> None:

    status = (
        '<span class="status-active">🟢 Active</span>'
        if active
        else '<span class="status-inactive">⚪ Not Active</span>'
    )

    st.markdown(
        f"""
<div class="employee-card">

<div class="employee-name">
👤 {employee}
</div>

<div class="employee-meta">
{status}<br><br>

<b>{completed_tasks}</b> completed task(s) this week<br>

<b>{total_minutes}</b> recorded this week

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# Active Employee Card
# =============================================================================

def render_active_employee(
    employee: str,
    project: str,
    task: str,
    clock_in: str,
    elapsed: str,
) -> None:

    st.markdown(
        f"""
<div class="active-card">

<div class="active-name">
🟢 {employee}
</div>

<div class="active-project">
{project}
</div>

<div class="active-task">
{task}
</div>

<div class="active-meta">
Clocked in: {clock_in}<br>
Elapsed: {elapsed}
</div>

</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# Empty State
# =============================================================================

def render_no_active_workers() -> None:

    st.info(
        "Nobody is currently tracking an active office-hour task."
    )

def render_active_task(
    project: str,
    task: str,
    started: str,
    elapsed: str,
    notes: str = "",
) -> None:
    """Render the currently active task card."""
    st.markdown(
        f"""
<div class="active-card">
    <div class="active-project">{project}</div>
    <div class="active-task">{task}</div>

    <div class="active-meta">
        Started: {started}<br>
        Elapsed: {elapsed}
    </div>

    <div class="task-notes">{notes}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_no_active_task() -> None:
    """Display a message when the employee has no active task."""
    st.info("No task is currently active.")


def render_task_card(
    project: str,
    task: str,
    notes: str = "",
) -> None:
    """Render a task waiting to be started."""
    st.markdown(
        f"""
<div class="task-card">
    <div class="task-project">{project}</div>
    <div class="task-title">{task}</div>
    <div class="task-notes">{notes}</div>
</div>
""",
        unsafe_allow_html=True,
    )
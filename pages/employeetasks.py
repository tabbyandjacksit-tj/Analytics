# ==========================================
# Imports
# ==========================================

from datetime import date, timedelta

import streamlit as st

from utils.styling.base import (
    apply_base_styles,
    render_hero,
)

from utils.styling.officehours import (
    apply_officehour_styles,
)

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Employee Office Hours",
    page_icon="images/logo.png",
    layout="wide",
)

apply_base_styles(max_width=1100)
apply_officehour_styles()

# ==========================================
# Employee Selection
# ==========================================

employee = st.session_state.get("selected_employee")

if employee is None:

    st.warning("Please choose an employee first.")

    if st.button("← Return to Office Hours"):

        st.switch_page("pages/officehours.py")

    st.stop()

# ==========================================
# Header
# ==========================================

render_hero(
    f"{employee}'s Office Hours",
    "Track projects, tasks, and completed work.",
)

# ==========================================
# Week Selection
# ==========================================

current_week = date.today() - timedelta(
    days=date.today().weekday()
)

week = st.selectbox(
    "Week",
    [
        current_week,
        current_week - timedelta(days=7),
        current_week - timedelta(days=14),
        current_week - timedelta(days=21),
    ],
    format_func=lambda value: value.strftime(
        "Week of %B %d, %Y"
    ),
)

# ==========================================
# Add Task
# ==========================================

st.markdown("## Add New Task")

with st.form("new_task"):

    project = st.text_input("Project")

    task = st.text_input("Task")

    notes = st.text_area("Notes")

    submitted = st.form_submit_button("Add Task")

if submitted:

    st.success(
        "Task would be added to Google Sheets."
    )

# ==========================================
# Active Task
# ==========================================

st.markdown("## Active Task")

st.info(
    "🟢 Building Office Hour Tracker\n\n"
    "Started 32 minutes ago"
)

left, right = st.columns(2)

with left:

    st.button(
        "Pause",
        use_container_width=True,
    )

with right:

    st.button(
        "Finish",
        use_container_width=True,
    )

# ==========================================
# Weekly Tasks
# ==========================================

st.markdown("## Weekly Tasks")

st.dataframe(
    [
        {
            "Project": "Analytics Hub",
            "Task": "Vendor Contacts",
            "Status": "Finished",
            "Minutes": 34,
        },
        {
            "Project": "Analytics Hub",
            "Task": "Office Hour Tracker",
            "Status": "Active",
            "Minutes": 18,
        },
        {
            "Project": "Shipping",
            "Task": "Carrier Testing",
            "Status": "To Do",
            "Minutes": "",
        },
    ],
    hide_index=True,
    use_container_width=True,
)
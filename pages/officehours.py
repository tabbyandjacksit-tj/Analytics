# ==========================================
# Imports
# ==========================================
import streamlit as st

from utils.styling.base import (
    apply_base_styles,
    render_hero,
)

from utils.styling.officehours import (
    apply_officehour_styles,
    render_employee_card,
    render_working_now_card,
)

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Office Hour Tracker",
    page_icon="images/logo.png",
    layout="wide",
)

apply_base_styles(max_width=1200)
apply_officehour_styles()

render_hero(
    "Office Hour Tracker",
    "Track office hour projects and see what everyone is working on.",
)

# ==========================================
# Load Data
# ==========================================

# Eventually these come from Google Sheets

employees = [
    "Maria",
    "Ashley",
    "Terry",
    "Emily",
]

active_tasks = [
    {
        "employee": "Maria",
        "project": "Analytics Hub",
        "task": "Building Office Hour Tracker",
        "minutes": 31,
    },
    {
        "employee": "Ashley",
        "project": "Inventory",
        "task": "MAP Pricing Review",
        "minutes": 58,
    },
]

# ==========================================
# Who's Working Now
# ==========================================

st.markdown("## Who's Working Now?")

if active_tasks:

    cols = st.columns(len(active_tasks))

    for col, task in zip(cols, active_tasks):

        with col:
            render_working_now_card(task)

else:

    st.info("Nobody is currently clocked into an office-hour task.")

# ==========================================
# Employees
# ==========================================

st.markdown("## Office Hour Employees")

cols = st.columns(2)

for index, employee in enumerate(employees):

    with cols[index % 2]:

        if render_employee_card(employee):

            st.session_state["selected_employee"] = employee

            st.switch_page("pages/employeetasks.py")
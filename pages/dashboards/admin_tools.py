# =======================================================================================
# Imports
# =======================================================================================
# =======================================================================================
# IMPORTS
# =======================================================================================
import streamlit as st
from utils.styling.base import apply_base_styles
from utils.styling.dashboard import (
    apply_dashboard_styles,
    render_dashboard_banner,
    render_dashboard_intro,
)
from utils.styling.home import (
    apply_home_styles,
    render_tool_card,
)
from utils.tools.images import image_to_base64
# =======================================================================================
# Page Configuration (sets title, icon, and layout of page)
# CSS Styles also imported/applied
# =======================================================================================
st.set_page_config(
    page_title="Admin Tools",
    page_icon="images/logo.png",
    layout="wide",
)
apply_base_styles(max_width=1160)
apply_home_styles()
apply_dashboard_styles()
render_dashboard_banner(
    title="Admin Tools",
    description=(
        "Access tools for employee management, data processing, "
        "and external platform updates."
    ),
)
render_dashboard_intro(
    eyebrow="Administrative Tools",
    title="Choose an Admin Tool",
    description=(
        "Select a tool below to manage employee activity, "
        "process reports, or update external platforms."
    ),
)
icons = { # Neeeds to be adjusted per each card created 
    "instacart": image_to_base64("images/item_report.png"),
    "customer_capture": image_to_base64("images/brand.png"),
    "office_tasks": image_to_base64("images/ordering.png"),
}
# =======================================================================================
# Admin Tools Links and Cards. This is super similar to home.py
# =======================================================================================
tools = [
    {
        "title": "Instacart Upload",
        "description": (
            "Prepare nine different inventory files and SFTP send them to Instacart."
        ),
        "status": "Available",
        "category": "Admin Tools",
        "icon": icons["instacart"],
        "page": "pages/admin/instacart.py",
        "enabled": True,
    },
    {
        "title": "Customer Capture Rate",
        "description": (
            "Review and manage employee customer-capture rates and see the current ranking."
        ),
        "status": "Available",
        "category": "Admin Tools",
        "icon": icons["customer_capture"],
        "page": "pages/admin/employeecapture.py",
        "enabled": True,
    },
    {
        "title": "Employee Office Hours",
        "description": (
            "Track and review at home office hour tasks"
        ),
        "status": "Available",
        "category": "Admin Tools",
        "icon": icons["office_tasks"],
        "page": "pages/admin/officehours/officehours.py",
        "enabled": True,
    },
]
# =======================================================================================
# Creates the dashboard tool card and renders them on the home page. Here is where each 
# category is created too! Each tool card is displayed in a 2-column layout with the 
# information created in the lists above. 
# =======================================================================================
for index in range(0, len(tools), 2):
    columns = st.columns(2, gap="large")

    for column, tool in zip(columns, tools[index:index + 2]):
        with column:
            render_tool_card(
                tool,
                key=f"admin_{tool['title'].lower().replace(' ', '_')}",
            )
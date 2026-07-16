# =======================================================================================
# Imports
# =======================================================================================

import streamlit as st

from utils.tools.images import image_to_base64
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


# =======================================================================================
# Page Configuration
# =======================================================================================

st.set_page_config(
    page_title="Admin Tools",
    page_icon="images/logo.png",
    layout="wide",
)


# =======================================================================================
# Apply Styles
# =======================================================================================

apply_base_styles(max_width=1160)
apply_home_styles()
apply_dashboard_styles()


# =======================================================================================
# Dashboard Header
# =======================================================================================
render_dashboard_banner(
    title="Admin Tools",
    description=(
        "Access administrative tools for employee management, "
        "data processing, and external platform updates."
    ),
)

render_dashboard_intro(
    eyebrow="Administrative Tools",
    title="Choose an Admin Tool",
    description="Select an administrative tool below to continue.",
)

# =======================================================================================
# Load Card Icons
# =======================================================================================

icons = {
    "instacart": image_to_base64("images/item_report.png"),
    "customer_capture": image_to_base64("images/brand.png"),
    "office_tasks": image_to_base64("images/ordering.png"),
}


# =======================================================================================
# Admin Tools
# =======================================================================================

tools = [
    {
        "title": "Instacart Upload",
        "description": (
            "Prepare store inventory files and send them to Instacart."
        ),
        "status": "Available",
        "category": "Admin Tools",
        "icon": icons["instacart"],
        "page": "pages/admin/instacart.py",
        "enabled": True,
    },
    {
        "title": "Employee Customer Capture",
        "description": (
            "Review and manage employee customer-capture information."
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
            "Review employee office-hour entries and assigned office tasks."
        ),
        "status": "Available",
        "category": "Admin Tools",
        "icon": icons["office_tasks"],
        "page": "pages/admin/officehours/.py",
        "enabled": True,
    },
]


# =======================================================================================
# Render Dashboard Cards
# =======================================================================================


for index in range(0, len(tools), 2):
    columns = st.columns(2, gap="large")

    for column, tool in zip(columns, tools[index:index + 2]):
        with column:
            render_tool_card(
                tool,
                key=f"admin_{tool['title'].lower().replace(' ', '_')}",
            )
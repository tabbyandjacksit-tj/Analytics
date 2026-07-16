# =======================================================================================
# Imports
# =======================================================================================

import streamlit as st

from utils.tools.images import image_to_base64
from utils.styling.base import apply_base_styles
from utils.styling.home import (
    apply_home_styles,
    render_category_title,
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


# =======================================================================================
# Dashboard Header
# =======================================================================================

st.markdown(
    """
    <div style="
        background-color: #1D5A3E;
        border-radius: 24px;
        padding: 34px 30px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 22px rgba(29, 90, 62, .18);
    ">
        <h1 style="
            color: #FFF9EF;
            margin: 0;
            font-size: 42px;
            font-weight: 900;
        ">
            Admin Tools
        </h1>

        <p style="
            color: rgba(255, 249, 239, .88);
            margin: 10px 0 0 0;
            font-size: 17px;
        ">
            Access restricted tools for data uploads and employee administration.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
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
        "page": "pages/admin/officehours/employeetasks.py",
        "enabled": True,
    },
]


# =======================================================================================
# Render Dashboard Cards
# =======================================================================================

render_category_title("Select an Admin Tool")

for index in range(0, len(tools), 2):
    columns = st.columns(2, gap="large")

    for column, tool in zip(columns, tools[index:index + 2]):
        with column:
            render_tool_card(
                tool,
                key=f"admin_{tool['title'].lower().replace(' ', '_')}",
            )
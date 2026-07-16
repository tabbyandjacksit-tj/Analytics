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
    page_title="Employee Resources",
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
            Employee Resources
        </h1>

        <p style="
            color: rgba(255, 249, 239, .88);
            margin: 10px 0 0 0;
            font-size: 17px;
        ">
            Find vendor information, company resources, and employee tools.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =======================================================================================
# Load Card Icons
# =======================================================================================

icons = {
    "links": image_to_base64("images/brand.png"),
    "vendor": image_to_base64("images/brand.png"),
    "map": image_to_base64("images/item_report.png"),
    "office_hours": image_to_base64("images/ordering.png"),
}


# =======================================================================================
# Employee Resource Tools
# =======================================================================================

tools = [
    {
        "title": "Helpful Links",
        "description": (
            "Open frequently used company documents, schedules, and resources."
        ),
        "status": "Available",
        "category": "Employee Resources",
        "icon": icons["links"],
        "page": "pages/resources/links.py",
        "enabled": True,
    },
    {
        "title": "Vendor Contact",
        "description": (
            "Search vendor contact information and review vendor details."
        ),
        "status": "Available",
        "category": "Employee Resources",
        "icon": icons["vendor"],
        "page": "pages/resources/vendorcontact.py",
        "enabled": True,
    },
    {
        "title": "MAP Information",
        "description": (
            "Review MAP pricing information and compliant brand resources."
        ),
        "status": "Available",
        "category": "Employee Resources",
        "icon": icons["map"],
        "page": "pages/resources/MAP.py",
        "enabled": True,
    },
    {
        "title": "Office Hour Tracker",
        "description": (
            "Track office-hour work and review assigned employee tasks."
        ),
        "status": "Available",
        "category": "Employee Resources",
        "icon": icons["office_hours"],
        "page": "pages/admin/officehours/officehours.py",
        "enabled": True,
    },
]


# =======================================================================================
# Render Dashboard Cards
# =======================================================================================

render_category_title("Select a Resource")

for index in range(0, len(tools), 2):
    columns = st.columns(2, gap="large")

    for column, tool in zip(columns, tools[index:index + 2]):
        with column:
            render_tool_card(
                tool,
                key=f"resource_{tool['title'].lower().replace(' ', '_')}",
            )
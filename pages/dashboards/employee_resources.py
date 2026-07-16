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
    page_title="Employee Resources",
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
    title="Employee Resources",
    description=(
        "Find vendor information, company documents, pricing resources, "
        "and tools that support daily operations."
    ),
)

render_dashboard_intro(
    eyebrow="Employee Resources",
    title="Choose a Resource",
    description="Select a resource below to view more information.",
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


for index in range(0, len(tools), 2):
    columns = st.columns(2, gap="large")

    for column, tool in zip(columns, tools[index:index + 2]):
        with column:
            render_tool_card(
                tool,
                key=f"resource_{tool['title'].lower().replace(' ', '_')}",
            )
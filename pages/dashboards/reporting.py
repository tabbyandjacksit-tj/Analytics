# ======================================================================================
# Imports
# ======================================================================================

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

# ======================================================================================
# Page Configuration
# ======================================================================================

st.set_page_config(
    page_title="Reporting",
    page_icon="images/logo.png",
    layout="wide",
)


# ======================================================================================
# Apply Styles
# ======================================================================================

apply_base_styles(max_width=1160)
apply_home_styles()
apply_dashboard_styles()


# ======================================================================================
# Page Banner
# ======================================================================================

render_dashboard_banner(
    title="Reporting Dashboard",
    description=(
        "Review sales, inventory, and operational information "
        "from one central location."
    ),
)

render_dashboard_intro(
    eyebrow="Reporting Tools",
    title="Choose a Report",
    description="Select a reporting tool below to get started.",
)


# =======================================================================================
# Load Card Icons
# =======================================================================================

icons = {
    "transfer": image_to_base64("images/item_report.png"),
    "brand": image_to_base64("images/brand.png"),
}


# =======================================================================================
# Reporting Tools
# =======================================================================================

tools = [
    {
        "title": "Dusty Report Transfer",
        "description": (
            "Review Dusty inventory and identify possible transfer locations."
        ),
        "status": "Coming Soon",
        "category": "Reporting",
        "icon": icons["transfer"],
        "page": "pages/reports/dusty.py",
        "enabled": False,
    },
    {
        "title": "Sales by Brand",
        "description": (
            "Review previous sales by brand and generate a sales report."
        ),
        "status": "Coming Soon",
        "category": "Reporting",
        "icon": icons["brand"],
        "page": "pages/reports/brandsale.py",
        "enabled": False,
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
                key=f"reporting_{tool['title'].lower().replace(' ', '_')}",
            )
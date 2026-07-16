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
    page_title="Reporting",
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
            Reporting
        </h1>

        <p style="
            color: rgba(255, 249, 239, .88);
            margin: 10px 0 0 0;
            font-size: 17px;
        ">
            Review sales, inventory, and operational information.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
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

render_category_title("Select a Report")

for index in range(0, len(tools), 2):
    columns = st.columns(2, gap="large")

    for column, tool in zip(columns, tools[index:index + 2]):
        with column:
            render_tool_card(
                tool,
                key=f"reporting_{tool['title'].lower().replace(' ', '_')}",
            )
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
# Page Configuration (sets title, icon, and layout of page)
# CSS Styles also imported/applied
# =======================================================================================
st.set_page_config(
    page_title="Ordering Tools",
    page_icon="images/logo.png",
    layout="wide",
)
apply_base_styles(max_width=1160)
apply_home_styles()
apply_dashboard_styles()
render_dashboard_banner(
    title="Ordering Tools",
    description=(
        "Create recommended orders and prepare vendor order templates "
        "using Lightspeed reports."
    ),
)
render_dashboard_intro(
    eyebrow="Ordering Tools",
    title="Choose an Ordering Tool",
    description="Select the order type you would like to prepare.",
)
icons = { # Neeeds to be adjusted per each card created 
    "major_order": image_to_base64("images/ordering.png"),
    "small_order": image_to_base64("images/small_order.png"),
}
# =======================================================================================
# Ordering Tools Links and Cards. This is super similar to home.py
# =======================================================================================
tools = [
    {
        "title": "Major Vendor Order",
        "description": (
            "Upload a Major Vendor Order Lightspeed report and generate a recommended order template."
        ),
        "status": "Available",
        "category": "Ordering Tools",
        "icon": icons["major_order"],
        "page": "pages/reports/MVO.py",
        "enabled": True,
    },
    {
        "title": "Small Vendor Order",
        "description": (
            "Upload a Small Vendor Order Lightspeed report and generate recommended order template."
        ),
        "status": "Available",
        "category": "Ordering Tools",
        "icon": icons["small_order"],
        "page": "pages/reports/SVO.py",
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
                key=f"ordering_{tool['title'].lower().replace(' ', '_')}",
            )
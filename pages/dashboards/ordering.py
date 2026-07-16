import streamlit as st

from utils.tools.images import image_to_base64
from utils.styling.base import apply_base_styles
from utils.styling.home import (
    apply_home_styles,
    render_category_title,
    render_dashboard_header,
    render_tool_card,
)

st.set_page_config(
    page_title="Ordering Tools",
    page_icon="images/logo.png",
    layout="wide",
)

apply_base_styles(max_width=1160)
apply_home_styles()

render_dashboard_header(
    title="Ordering Tools",
    subtitle="Create and manage vendor orders.",
)

icons = {
    "major": image_to_base64("images/ordering.png"),
    "small": image_to_base64("images/small_order.png"),
}

tools = [
    {
        "title": "Major Vendor Order",
        "description": (
            "Upload a Major Vendor Order report and generate an order template."
        ),
        "status": "Available",
        "category": "Ordering Tools",
        "icon": icons["major"],
        "page": "pages/reports/MVO.py",
        "enabled": True,
    },
    {
        "title": "Small Vendor Order",
        "description": (
            "Upload a Small Vendor Order report and generate an order template."
        ),
        "status": "Available",
        "category": "Ordering Tools",
        "icon": icons["small"],
        "page": "pages/reports/SVO.py",
        "enabled": True,
    },
]

render_category_title("Select a Tool")

cols = st.columns(2, gap="large")

for col, tool in zip(cols, tools):
    with col:
        render_tool_card(
            tool,
            key=f"open_{tool['title'].lower().replace(' ', '_')}",
        )
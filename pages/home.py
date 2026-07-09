import streamlit as st

from utils.images import image_to_base64
from utils.styling.base import apply_base_styles
from utils.styling.home import (
    apply_home_styles,
    render_category_title,
    render_dashboard_header,
    render_footer,
    render_home_banner,
    render_tool_card,
)


st.set_page_config(
    page_title="Tabby & Jack's Analytics Hub",
    page_icon="images/logo.png",
    layout="wide",
)

apply_base_styles(max_width=1160)
apply_home_styles()

logo = image_to_base64("images/logo.png")

icons = {
    "ordering": image_to_base64("images/ordering.png"),
    "transfer": image_to_base64("images/item_report.png"),
    "small": image_to_base64("images/small_order.png"),
    "brand": image_to_base64("images/brand.png"),
}

tools = [
    {
        "title": "Major Vendor Order",
        "description": "Upload a Major Vendor Order Lightspeed report and generate an order template",
        "status": "Available",
        "category": "Ordering Tools",
        "icon": icons["ordering"],
        "page": "pages/MVO.py",
        "enabled": True,
    },
    {
        "title": "Small Vendor Order",
        "description": "Upload a Small Vendor Order Lightspeed report and generate an order template",
        "status": "Available",
        "category": "Ordering Tools",
        "icon": icons["small"],
        "page": "pages/SVO.py",
        "enabled": True,
    },
    {
        "title": "Dusty Report Transfer",
        "description": "See where Dusty Inventory can go!",
        "status": "Coming Soon",
        "category": "Inventory Tools",
        "icon": icons["transfer"],
        "page": "pages/dusty.py",
        "enabled": False,
    },
    {
        "title": "Sales by Brand",
        "description": "See previous sales by brand and generate a report",
        "status": "Coming Soon",
        "category": "Inventory Tools",
        "icon": icons["brand"],
        "page": "pages/brandsale.py",
        "enabled": False,
    },
    {
        "title": "Vendor Contact Sheet",
        "description": "Search for all of our different vendors and get their contact information",
        "status": "Available",
        "category": "Office Hour Tools",
        "icon": icons["brand"],
        "page": "pages/vendorcontact.py",
        "enabled": True,
    },
    {
        "title": "Office Hour Tracker",
        "description": "Exclusively for work-from-home employees to track their working office hours.",
        "status": "Coming Soon",
        "category": "Office Hour Tools",
        "icon": icons["brand"],
        "page": "pages/officehour.py",
        "enabled": False,
    },
]

categories = ["Ordering Tools", "Inventory Tools", "Office Hour Tools"]

render_home_banner(logo)
render_dashboard_header()

for category in categories:
    category_tools = [tool for tool in tools if tool["category"] == category]

    render_category_title(category)

    for i in range(0, len(category_tools), 2):
        cols = st.columns(2, gap="large")

        for col, tool in zip(cols, category_tools[i:i + 2]):
            with col:
                render_tool_card(
                    tool,
                    key=f"open_{tool['title'].lower().replace(' ', '_')}",
                )

render_footer()
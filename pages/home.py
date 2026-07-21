# =======================================================================================
# Imports
# =======================================================================================
import streamlit as st
from utils.tools.images import image_to_base64
from utils.styling.base import apply_base_styles
from utils.styling.home import (
    apply_home_styles,
    render_dashboard_header,
    render_footer,
    render_home_banner,
    render_tool_card,
)
# =======================================================================================
# Page Configuration (sets title, icon, and layout of page)
# CSS Styles also imported/applied
# =======================================================================================
st.set_page_config(
    page_title="Tabby & Jack's Analytics Hub",
    page_icon="images/logo.png",
    layout="wide",
)

logo = image_to_base64("images/logo.png")

render_home_banner(logo) # from utils.styling.home 
render_dashboard_header() # from utils.styling.home
apply_base_styles(max_width=1160) # from utils.styling.base
apply_home_styles() # from utils.styling.base

# =======================================================================================
# Load in different images and icons for the page
# image_to_base64 function converts the image to a base64 string so it can be used in HTML/CSS
# =======================================================================================
icons = {
    "ordering": image_to_base64("images/ordering.png"),
    "transfer": image_to_base64("images/item_report.png"),
    "small": image_to_base64("images/small_order.png"),
    "brand": image_to_base64("images/brand.png"),
}

# =======================================================================================
# Define the different tool cards that will be displayed on the home page. 
# Each tool has a title, description, status, category, icon, page link, and enabled status and 
# represents one card on the home page. 
# =======================================================================================
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
        "description": "See the best place for your Dusty Inventory to go!",
        "status": "Coming Soon",
        "category": "Inventory Tools",
        "icon": icons["transfer"],
        "page": "pages/dusty.py",
        "enabled": False,
    },
    {
        "title": "Sales by Brand",
        "description": "See previous months sales per brand and generate a report to see what should be reordered!",
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
        "status": "Availiable",
        "category": "Office Hour Tools",
        "icon": icons["brand"],
        "page": "pages/admin/officehours/officehours.py",
        "enabled": True,
    },
]
categories = ["Ordering Tools", "Inventory Tools", "Office Hour Tools"] # Where you can create different categories.
# TODO: Expand out so that the categories = what the navigation is, and each click takes you to THAT page! 

# =======================================================================================
# Creates the dashboard tool card and renders them on the home page. Here is where each 
# category is created too! Each tool card is displayed in a 2-column layout with the 
# information created in the lists above. 
# =======================================================================================
for category in categories:
    category_tools = [tool for tool in tools if tool["category"] == category]
    for i in range(0, len(category_tools), 2):
        cols = st.columns(2, gap="large")

        for col, tool in zip(cols, category_tools[i:i + 2]):
            with col:
                render_tool_card(tool, key=f"open_{tool['title'].lower().replace(' ', '_')}",)

        st.markdown(
            "<div style='height: 16px;'></div>",
            unsafe_allow_html=True,
        )
categories = ["Ordering Tools", "Inventory Tools", "Office Hour Tools"] # Where you can create different categories.
# TODO: Expand out so that the categories = what the navigation is, and each click takes you to THAT page! 

render_footer()
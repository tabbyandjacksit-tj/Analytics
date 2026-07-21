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
    render_dashboard_card,
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

apply_base_styles(max_width=1160)
apply_home_styles()
logo = image_to_base64("images/logo.png")
render_home_banner(logo)
render_dashboard_header()

# =======================================================================================
# Load in different images and icons for the page
# image_to_base64 function converts the image to a base64 string so it can be used in HTML/CSS
# =======================================================================================
icons = {
    "ordering": image_to_base64("images/ordering.png"),
    "reporting": image_to_base64("images/item_report.png"),
    "resources": image_to_base64("images/brand.png"),
    "admin": image_to_base64("images/admin.png"),
}

# =======================================================================================
# Define the different tool cards that will be displayed on the home page. 
# Each tool has a title, description, status, category, icon, page link, and enabled status and 
# represents one card on the home page. 
# =======================================================================================
dashboards = [
    {
        "title": "Ordering Tools",
        "description": (
            "Create major/small vendor orders and access tools used "
            "for inventory ordering and inventory control."
        ),
        "icon": icons["ordering"],
        "page": "pages/dashboards/ordering.py",
        "enabled": True,
    },
    {
        "title": "Reporting",
        "description": (
            "Review sales reports, inventory, and other "
            "reports from one central location."
        ),
        "icon": icons["reporting"],
        "page": "pages/dashboards/reporting.py",
        "enabled": True,
    },
    {
        "title": "Employee Resources",
        "description": (
            "Find vendor contacts, MAP information, "
            "helpful links, and employee resources."
        ),
        "icon": icons["resources"],
        "page": "pages/dashboards/employee_resources.py",
        "enabled": True,
    },
    {
        "title": "Admin Tools",
        "description": (
            "Access internal operational management tools. "
            "Some tools are limited to which users can access them."
        ),
        "icon": icons["admin"],
        "page": "pages/dashboards/admin_tools.py",
        "enabled": True,
    },
]

# categories = ["Ordering Tools", "Inventory Tools", "Office Hour Tools"] # Where you can create different categories.
# TODO: Expand out so that the categories = what the navigation is, and each click takes you to THAT page! 

# =======================================================================================
# Creates the dashboard tool card and renders them on the home page. Here is where each 
# category is created too! Each tool card is displayed in a 2-column layout with the 
# information created in the lists above. 
# =======================================================================================
for i in range(0, len(dashboards), 2):

    cols = st.columns(2, gap="large")

    for col, dashboard in zip(
        cols,
        dashboards[i:i + 2],
    ):
        with col:
            render_dashboard_card(
                dashboard,
                key=(
                    f"open_"
                    f"{dashboard['title'].lower().replace(' ', '_')}"
                ),
            )

    st.markdown(
        "<div style='height: 18px;'></div>",
        unsafe_allow_html=True,
    )

render_footer()
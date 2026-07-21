# ======================================================================================
# Imports
# ======================================================================================

import streamlit as st

from utils.auth import (
    render_login_gate,
    render_logout,
)


# ======================================================================================
# App Configuration
# ======================================================================================

st.set_page_config(
    page_title="Tabby & Jack's Analytics",
    page_icon="images/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ======================================================================================
# Employee Authentication
# ======================================================================================

try:
    authenticator = render_login_gate()

except Exception as exc:
    st.error("The employee login system could not be loaded.")
    st.exception(exc)
    st.stop()


# ======================================================================================
# Page Registration
# ======================================================================================

pages = {
    # ------------------------------------------------------------------
    # Main dashboard pages
    # ------------------------------------------------------------------

    "Home": st.Page(
        "pages/home.py",
        title="Home",
        icon=":material/home:",
        default=True,
    ),

    "Ordering Tools": st.Page(
        "pages/dashboards/ordering.py",
        title="Ordering Tools",
        icon=":material/shopping_cart:",
    ),

    "Reporting": st.Page(
        "pages/dashboards/reporting.py",
        title="Reporting",
        icon=":material/analytics:",
    ),

    "Employee Resources": st.Page(
        "pages/dashboards/employee_resources.py",
        title="Employee Resources",
        icon=":material/groups:",
    ),

    "Admin Tools": st.Page(
        "pages/dashboards/admin_tools.py",
        title="Admin Tools",
        icon=":material/admin_panel_settings:",
    ),

    # ------------------------------------------------------------------
    # Ordering tools
    # ------------------------------------------------------------------

    "Major Vendor Order": st.Page(
        "pages/reports/MVO.py",
        title="Major Vendor Order",
        icon=":material/shopping_cart:",
        visibility="hidden",
    ),

    "Small Vendor Order": st.Page(
        "pages/reports/SVO.py",
        title="Small Vendor Order",
        icon=":material/shopping_basket:",
        visibility="hidden",
    ),

    # ------------------------------------------------------------------
    # Reporting tools
    # ------------------------------------------------------------------

    "Dusty Report Transfer": st.Page(
        "pages/reports/dusty.py",
        title="Dusty Report Transfer",
        icon=":material/move_item:",
        visibility="hidden",
    ),

    "Sales by Brand": st.Page(
        "pages/reports/brandsale.py",
        title="Sales by Brand",
        icon=":material/filter_list:",
        visibility="hidden",
    ),

    # ------------------------------------------------------------------
    # Employee resources
    # ------------------------------------------------------------------

    "Helpful Links": st.Page(
        "pages/resources/links.py",
        title="Helpful Links",
        icon=":material/link:",
        visibility="hidden",
    ),

    "Vendor Contact": st.Page(
        "pages/resources/vendorcontact.py",
        title="Vendor Contact",
        icon=":material/contact_page:",
        visibility="hidden",
    ),

    "MAP Information": st.Page(
        "pages/resources/MAP.py",
        title="MAP Information",
        icon=":material/price_check:",
        visibility="hidden",
    ),

    "Office Hour Tracker": st.Page(
        "pages/admin/officehours/officehours.py",
        title="Office Hour Tracker",
        icon=":material/schedule:",
        visibility="hidden",
    ),

    # ------------------------------------------------------------------
    # Admin tools
    # ------------------------------------------------------------------

    "Instacart Upload": st.Page(
        "pages/admin/instacart.py",
        title="Instacart Upload",
        icon=":material/upload_file:",
        visibility="hidden",
    ),

    "Employee Customer Capture": st.Page(
        "pages/admin/employeecapture.py",
        title="Employee Customer Capture",
        icon=":material/person:",
        visibility="hidden",
    ),

    "Employee Office Hours": st.Page(
        "pages/admin/officehours/employeetasks.py",
        title="Employee Office Hours",
        icon=":material/task_alt:",
        visibility="hidden",
    ),

    # ------------------------------------------------------------------
    # Account
    # ------------------------------------------------------------------

    "Account": st.Page(
        "pages/account.py",
        title="Account Settings",
        icon=":material/manage_accounts:",
        visibility="hidden",
    ),
}


# ======================================================================================
# Searchable Tool Links
# ======================================================================================

report_links = {
    "Major Vendor Order": "pages/reports/MVO.py",
    "Small Vendor Order": "pages/reports/SVO.py",
    "Dusty Report Transfer": "pages/reports/dusty.py",
    "Sales by Brand": "pages/reports/brandsale.py",
    "Helpful Links": "pages/resources/links.py",
    "Vendor Contact": "pages/resources/vendorcontact.py",
    "MAP Information": "pages/resources/MAP.py",
    "Office Hour Tracker": "pages/admin/officehours/officehours.py",
    "Instacart Upload": "pages/admin/instacart.py",
    "Employee Customer Capture": "pages/admin/employeecapture.py",
    "Employee Office Hours": "pages/admin/officehours/employeetasks.py",
    "Account Settings": "pages/account.py",
}


# ======================================================================================
# App and Sidebar Styles
# ======================================================================================

st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {
        background: #5C8067;
        border-right: none;
    }

    section[data-testid="stSidebar"] * {
        color: #FFF9EF !important;
    }

    section[data-testid="stSidebar"] input {
        background: #FFF9EF !important;
        color: #1D5A3E !important;
        border: 1px solid #F3A653 !important;
        border-radius: 10px !important;
    }

    section[data-testid="stSidebar"] input::placeholder {
        color: #777777 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 249, 239, 0.25);
    }

    section[data-testid="stSidebar"]
    div[data-testid="stButton"] button {
        background-color: #C98335 !important;
        color: #FFF9EF !important;
        border: 1px solid #C98335 !important;
        border-radius: 12px !important;
        min-height: 42px !important;
        font-weight: 800 !important;
    }

    section[data-testid="stSidebar"]
    div[data-testid="stButton"] button:hover {
        background-color: #F3A653 !important;
        color: #1D5A3E !important;
        border-color: #F3A653 !important;
    }

    .sidebar-title {
        color: #FFF9EF;
        font-size: 1.75rem;
        font-weight: 900;
        margin-top: 0.2rem;
    }

    .sidebar-subtitle {
        color: #FFF9EF;
        font-size: 0.85rem;
        opacity: 0.85;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stDecoration"] {
        display: none;
    }

    button[data-testid="stBaseButton-headerNoPadding"] {
        display: none !important;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ======================================================================================
# Sidebar Navigation Helper
# ======================================================================================

def sidebar_nav_button(
    label: str,
    page_path: str,
    key: str | None = None,
) -> None:
    """
    Display a full-width sidebar navigation button.

    Parameters
    ----------
    label:
        Text and optional Material icon displayed on the button.

    page_path:
        Page path registered in the pages dictionary.

    key:
        Optional unique Streamlit widget key.
    """

    button_key = key or f"nav_{page_path}"

    if st.button(
        label,
        use_container_width=True,
        key=button_key,
    ):
        st.switch_page(page_path)


# ======================================================================================
# Custom Sidebar
# ======================================================================================

with st.sidebar:

    left_column, center_column, right_column = st.columns([1, 2, 1])

    with center_column:
        st.image(
            "images/logo.png",
            width=200,
        )

    st.markdown(
        """
        <div style="text-align: center;">
            <div class="sidebar-title">Tabby & Jack's</div>
            <div class="sidebar-subtitle">Analytics Hub</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### :material/search: Find a Report")

    search = st.text_input(
        "Search",
        placeholder="Search reports...",
        label_visibility="collapsed",
    )

    if search:
        search_term = search.strip().lower()

        matches = {
            name: page_path
            for name, page_path in report_links.items()
            if search_term in name.lower()
        }

        st.markdown("**Results**")

        if matches:
            for result_number, (name, page_path) in enumerate(
                matches.items()
            ):
                sidebar_nav_button(
                    label=f"Open {name}",
                    page_path=page_path,
                    key=f"search_{result_number}_{page_path}",
                )
        else:
            st.caption("Sorry! That tool does not exist.")

    st.divider()

    st.markdown("### Navigation")

    sidebar_nav_button(
        ":material/home: Home",
        "pages/home.py",
    )

    sidebar_nav_button(
        ":material/analytics: Reporting",
        "pages/dashboards/reporting.py",
    )

    sidebar_nav_button(
        ":material/shopping_cart: Ordering Tools",
        "pages/dashboards/ordering.py",
    )
    sidebar_nav_button(
        ":material/groups: Employee Resources",
        "pages/dashboards/employee_resources.py",
    )

    sidebar_nav_button(
        ":material/admin_panel_settings: Admin Tools",
        "pages/dashboards/admin_tools.py",
    )

    st.divider()

    sidebar_nav_button(
        ":material/manage_accounts: Account Settings",
        "pages/account.py",
    )

    render_logout(authenticator)


# ======================================================================================
# Run Navigation
# ======================================================================================

navigation = st.navigation(
    list(pages.values()),
    position="hidden",
)

navigation.run()
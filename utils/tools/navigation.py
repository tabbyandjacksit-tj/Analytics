from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit as st


# =============================================================================
# Master Page Dictionary
# =============================================================================

PAGE_CONFIG: dict[str, dict[str, Any]] = {
    # -------------------------------------------------------------------------
    # Main pages
    # -------------------------------------------------------------------------
    "home": {
        "title": "Home",
        "path": "pages/home.py",
        "icon": ":material/home:",
        "parent": None,
        "group": "Main",
        "sidebar": True,
        "searchable": False,
        "default": True,
    },

    "ordering": {
        "title": "Ordering Tools",
        "path": "pages/dashboards/ordering.py",
        "icon": ":material/shopping_cart:",
        "parent": "home",
        "group": "Main",
        "sidebar": True,
        "searchable": False,
    },

    "reporting": {
        "title": "Reporting",
        "path": "pages/dashboards/reporting.py",
        "icon": ":material/analytics:",
        "parent": "home",
        "group": "Main",
        "sidebar": True,
        "searchable": False,
    },

    "employee_resources": {
        "title": "Employee Resources",
        "path": "pages/dashboards/employee_resources.py",
        "icon": ":material/groups:",
        "parent": "home",
        "group": "Main",
        "sidebar": True,
        "searchable": False,
    },

    "admin_tools": {
        "title": "Admin Tools",
        "path": "pages/dashboards/admin_tools.py",
        "icon": ":material/admin_panel_settings:",
        "parent": "home",
        "group": "Main",
        "sidebar": True,
        "searchable": False,
    },

    # -------------------------------------------------------------------------
    # Ordering tools
    # -------------------------------------------------------------------------
    "major_vendor_order": {
        "title": "Major Vendor Order",
        "path": "pages/reports/MVO.py",
        "icon": ":material/shopping_cart:",
        "parent": "ordering",
        "group": "Ordering Tools",
        "sidebar": False,
        "searchable": True,
    },

    "small_vendor_order": {
        "title": "Small Vendor Order",
        "path": "pages/reports/SVO.py",
        "icon": ":material/shopping_basket:",
        "parent": "ordering",
        "group": "Ordering Tools",
        "sidebar": False,
        "searchable": True,
    },

    # -------------------------------------------------------------------------
    # Reporting tools
    # -------------------------------------------------------------------------
    "dusty_report": {
        "title": "Dusty Report Transfer",
        "path": "pages/reports/dusty.py",
        "icon": ":material/move_item:",
        "parent": "reporting",
        "group": "Reporting",
        "sidebar": False,
        "searchable": True,
    },

    "sales_by_brand": {
        "title": "Sales by Brand",
        "path": "pages/reports/brandsale.py",
        "icon": ":material/filter_list:",
        "parent": "reporting",
        "group": "Reporting",
        "sidebar": False,
        "searchable": True,
    },

    "sales_by_hour": {
        "title": "Sales by Hour",
        "path": "pages/reports/salesbyhour.py",
        "icon": ":material/calendar_clock:",
        "parent": "reporting",
        "group": "Reporting",
        "sidebar": False,
        "searchable": True,
    },

    # -------------------------------------------------------------------------
    # Employee resources
    # -------------------------------------------------------------------------
    "helpful_links": {
        "title": "Helpful Links",
        "path": "pages/resources/links.py",
        "icon": ":material/link:",
        "parent": "employee_resources",
        "group": "Employee Resources",
        "sidebar": False,
        "searchable": True,
    },

    "vendor_contact": {
        "title": "Vendor Contact",
        "path": "pages/resources/vendorcontact.py",
        "icon": ":material/contact_page:",
        "parent": "employee_resources",
        "group": "Employee Resources",
        "sidebar": False,
        "searchable": True,
    },

    "map_information": {
        "title": "MAP Information",
        "path": "pages/resources/MAP.py",
        "icon": ":material/price_check:",
        "parent": "employee_resources",
        "group": "Employee Resources",
        "sidebar": False,
        "searchable": True,
    },

    "office_hours": {
        "title": "Office Hour Tracker",
        "path": "pages/admin/officehours/officehours.py",
        "icon": ":material/schedule:",
        "parent": "employee_resources",
        "group": "Employee Resources",
        "sidebar": False,
        "searchable": True,
    },

    # -------------------------------------------------------------------------
    # Admin tools
    # -------------------------------------------------------------------------
    "instacart": {
        "title": "Instacart Upload",
        "path": "pages/admin/instacart.py",
        "icon": ":material/upload_file:",
        "parent": "admin_tools",
        "group": "Admin Tools",
        "sidebar": False,
        "searchable": True,
    },

    "employee_capture": {
        "title": "Employee Customer Capture",
        "path": "pages/admin/employeecapture.py",
        "icon": ":material/person:",
        "parent": "admin_tools",
        "group": "Admin Tools",
        "sidebar": False,
        "searchable": True,
    },

    "employee_tasks": {
        "title": "Employee Office Hours",
        "path": "pages/admin/officehours/employeetasks.py",
        "icon": ":material/task_alt:",
        "parent": "admin_tools",
        "group": "Admin Tools",
        "sidebar": False,
        "searchable": True,
    },

    "sort_grooming": {
        "title": "Verify Grooming Appointments",
        "path": "pages/admin/sortgrooming.py",
        "icon": ":material/sort:",
        "parent": "admin_tools",
        "group": "Admin Tools",
        "sidebar": False,
        "searchable": True,
    },

    # -------------------------------------------------------------------------
    # Account
    # -------------------------------------------------------------------------
    "account": {
        "title": "Account Settings",
        "path": "pages/account.py",
        "icon": ":material/manage_accounts:",
        "parent": None,
        "group": "Account",
        "sidebar": True,
        "searchable": True,
    },
}


# =============================================================================
# Page Lookup Helpers
# =============================================================================

def get_page(page_id: str) -> dict[str, Any]:
    """Return one page configuration."""

    try:
        return PAGE_CONFIG[page_id]
    except KeyError as exc:
        raise KeyError(
            f"Unknown page ID: {page_id}"
        ) from exc


def find_page_id(current_file: str) -> str | None:
    """Find a page ID using the current page's file path."""

    current_path = Path(current_file).resolve()

    for page_id, page in PAGE_CONFIG.items():
        configured_path = Path(page["path"])

        if (
            current_path.name == configured_path.name
            and configured_path.as_posix() in current_path.as_posix()
        ):
            return page_id

    # Filename fallback
    for page_id, page in PAGE_CONFIG.items():
        if current_path.name == Path(page["path"]).name:
            return page_id

    return None


# =============================================================================
# Streamlit Page Registration
# =============================================================================

def build_streamlit_pages() -> list[st.Page]:
    """Create all Streamlit pages from PAGE_CONFIG."""

    registered_pages: list[st.Page] = []

    for page in PAGE_CONFIG.values():
        page_arguments = {
            "page": page["path"],
            "title": page["title"],
            "icon": page.get("icon"),
            "default": page.get("default", False),
        }

        if not page.get("sidebar", False):
            page_arguments["visibility"] = "hidden"

        registered_pages.append(
            st.Page(**page_arguments)
        )

    return registered_pages


# =============================================================================
# Sidebar Helpers
# =============================================================================

def get_sidebar_pages() -> dict[str, dict[str, Any]]:
    """Return pages that should appear in the custom sidebar."""

    return {
        page_id: page
        for page_id, page in PAGE_CONFIG.items()
        if page.get("sidebar", False)
    }


def get_searchable_pages() -> dict[str, dict[str, Any]]:
    """Return pages that should appear in search."""

    return {
        page_id: page
        for page_id, page in PAGE_CONFIG.items()
        if page.get("searchable", False)
    }


def navigate_to(page_id: str) -> None:
    """Navigate using a page ID."""

    page = get_page(page_id)
    st.switch_page(page["path"])


# =============================================================================
# Breadcrumbs
# =============================================================================

def build_breadcrumbs(page_id: str) -> list[tuple[str, str | None]]:
    """Build a breadcrumb chain by following parent page IDs."""

    breadcrumbs: list[tuple[str, str | None]] = []
    visited: set[str] = set()

    current_id: str | None = page_id

    while current_id is not None:
        if current_id in visited:
            raise RuntimeError(
                f"Circular breadcrumb parent found at: {current_id}"
            )

        visited.add(current_id)

        page = get_page(current_id)

        breadcrumbs.append(
            (
                page["title"],
                page["path"],
            )
        )

        current_id = page.get("parent")

    breadcrumbs.reverse()

    # Current page should not link to itself
    if breadcrumbs:
        current_title, _ = breadcrumbs[-1]
        breadcrumbs[-1] = (current_title, None)

    return breadcrumbs


def render_breadcrumb(current_file: str) -> None:
    """Render compact automatic breadcrumbs for the current page."""

    page_id = find_page_id(current_file)

    if page_id is None:
        return

    breadcrumbs = build_breadcrumbs(page_id)
    parent_id = PAGE_CONFIG[page_id].get("parent")

    parts: list[str] = []

    if parent_id:
        parent_page = get_page(parent_id)

        parts.append(
            f"""
            <a
                href="/{Path(parent_page["path"]).stem}"
                target="_self"
                class="breadcrumb-back"
                title="Back to {parent_page["title"]}"
            >
                ←
            </a>
            """
        )

    for index, (title, page_path) in enumerate(breadcrumbs):
        is_current = page_path is None

        if index > 0:
            parts.append('<span class="breadcrumb-divider">/</span>')

        if is_current:
            parts.append(
                f'<span class="breadcrumb-current">{title}</span>'
            )
        else:
            slug = Path(page_path).stem

            parts.append(
                f"""
                <a
                    href="/{slug}"
                    target="_self"
                    class="breadcrumb-link"
                >
                    {title}
                </a>
                """
            )

    breadcrumb_html = "".join(parts)

    st.markdown(
        f"""
        <style>
        .breadcrumb-row {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: -0.4rem;
            margin-bottom: 0.9rem;
            font-size: 0.82rem;
            line-height: 1;
        }}

        .breadcrumb-row a {{
            text-decoration: none !important;
        }}

        .breadcrumb-back {{
            color: #5C7A58 !important;
            font-size: 1rem;
            font-weight: 800;
            margin-right: 0.15rem;
        }}

        .breadcrumb-link {{
            color: #5C7A58 !important;
            font-weight: 700;
        }}

        .breadcrumb-back:hover,
        .breadcrumb-link:hover {{
            color: #EF8B1D !important;
        }}

        .breadcrumb-divider {{
            color: #B4A993;
            font-weight: 500;
        }}

        .breadcrumb-current {{
            color: #1D5A3E;
            font-weight: 800;
        }}
        </style>

        <div class="breadcrumb-row">
            {breadcrumb_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
# ======================================================================================
# Imports
# ======================================================================================

import streamlit as st

from utils.auth import (
    render_login_gate,
    render_logout,
)

from utils.tools.navigation import (
    build_streamlit_pages,
    get_searchable_pages,
    get_sidebar_pages,
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
# Page Registration
# ======================================================================================


registered_pages = build_streamlit_pages()

navigation = st.navigation(
    registered_pages,
    position="hidden",
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
# Searchable Tool Links
# ======================================================================================

searchable_pages = get_searchable_pages()


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
            page_id: page
            for page_id, page in searchable_pages.items()
            if search_term in page["title"].lower()
        }

        st.markdown("**Results**")

        if matches:
            for result_number, (page_id, page) in enumerate(
                matches.items()
            ):
                sidebar_nav_button(
                    label=f"Open {page['title']}",
                    page_path=page["path"],
                    key=f"search_{result_number}_{page_id}",
                )
        else:
            st.caption("Sorry! That tool does not exist.")

    st.divider()

    st.markdown("### Navigation")

    sidebar_pages = get_sidebar_pages()

    for page_id, page in sidebar_pages.items():
        if page_id == "account":
            continue

        label = f"{page['icon']} {page['title']}"

        sidebar_nav_button(
            label=label,
            page_path=page["path"],
            key=f"sidebar_{page_id}",
        )

    st.divider()

    account_page = sidebar_pages["account"]

    sidebar_nav_button(
        label=(
            f"{account_page['icon']} "
            f"{account_page['title']}"
        ),
        page_path=account_page["path"],
        key="sidebar_account",
    )

    render_logout(authenticator)


# ======================================================================================
# Run Navigation
# ======================================================================================


navigation.run()
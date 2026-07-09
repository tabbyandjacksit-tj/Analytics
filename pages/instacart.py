from pathlib import Path

import streamlit as st

from utils.instacart import (
    create_instacart_files,
    upload_files_to_instacart,
)
from utils.styling.base import apply_base_styles
from utils.styling.instacart import (
    apply_instacart_styles,
    render_instacart_header,
    render_instacart_link,
    render_report_help_card,
)


st.set_page_config(
    page_title="Instacart Upload",
    page_icon="images/logo.png",
    layout="wide",
)

PASSWORD = st.secrets["INSTACART_PASSWORD"]


# ======================================================
# Authentication
# ======================================================

if "instacart_authenticated" not in st.session_state:
    st.session_state.instacart_authenticated = False


@st.dialog("Need Access?")
def access_help():
    st.write(
        """
This page is restricted to specific authorized employees.

If you need access or have any questions, please contact:

**Maria Swenson**
"""
    )


if not st.session_state.instacart_authenticated:

    password = st.text_input(
        "Enter password to access this page",
        type="password",
    )

    if st.button("Unlock", use_container_width=True):

        if password == PASSWORD:
            st.session_state.instacart_authenticated = True
            st.rerun()

        st.error("Incorrect password.")

    if st.button("Need Access?", use_container_width=True):
        access_help()

    st.stop()


# ======================================================
# Page Styling
# ======================================================

apply_base_styles()
apply_instacart_styles()


# ======================================================
# Page Header
# ======================================================

render_instacart_header()
render_report_help_card()


# ======================================================
# File Upload
# ======================================================

report_file = st.file_uploader(
    "Upload CSV Here",
    type=["csv"],
    label_visibility="collapsed",
)

password = st.text_input(
    "Enter Instacart SFTP Password",
    type="password",
)

sales_file = Path("data/sales.csv")


# ======================================================
# Upload
# ======================================================

if report_file and password:

    if st.button(
        "Configure Data & Upload to Instacart",
        use_container_width=True,
    ):

        output_folder = Path("temp_instacart_files")
        output_folder.mkdir(exist_ok=True)

        created_files = create_instacart_files(
            report_file,
            sales_file,
            output_folder,
        )

        uploaded = upload_files_to_instacart(
            created_files,
            password,
        )

        st.success(
            f"Successfully uploaded all {len(uploaded)} store files to Instacart."
        )

elif report_file:

    st.warning(
        "Please enter the Instacart SFTP password before uploading."
    )


# ======================================================
# Footer
# ======================================================

render_instacart_link()
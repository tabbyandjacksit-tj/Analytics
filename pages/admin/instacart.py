# =======================================================================================
# Imports
# =======================================================================================
from pathlib import Path
import streamlit as st
from utils.reporting.instacart import (
    create_instacart_files,
    upload_files_to_instacart,
)
from utils.tools.secrets import get_secret
from utils.components.headers import render_section_header
from utils.styling.base import (
    apply_base_styles,
    render_hero,
)
from utils.styling.components import apply_component_styles
from utils.styling.instacart import (
    apply_instacart_styles,
    render_instacart_link,
    render_report_hlp_card,
)
from utils.tools.navigation import render_breadcrumb
from utils.auth.users import require_role
# =======================================================================================
# Page Configuration (sets title, icon, and layout of page)
# CSS Styles also imported/applied
# =======================================================================================
require_role("IT Admin")  # Restrict access to users with the "IT Admin" role

st.set_page_config(
    page_title="Instacart Upload",
    page_icon="images/logo.png",
    layout="wide",
)
apply_base_styles()
apply_component_styles()
apply_instacart_styles() 
render_breadcrumb(__file__)
render_hero(
    "Instacart Upload",
    (
        "Configure your Lightspeed inventory report and upload "
        "the store files to Instacart."
    ),
)
# ======================================================
# Upload the Lightspeed Item report and input SFTP password 
# ======================================================
report_file = st.file_uploader( # Creates the upload box
    "Upload CSV Here",
    type=["csv"],
    label_visibility="collapsed",
)
password = st.text_input( # Creates the password input box (SFTP password for Instacart) 
    "Enter Instacart SFTP Password",
    type="password",
)
sales_file = Path("data/sales.csv") 
# ======================================================
# Edit the data in accordance with utils/instacart.py and upload to Instacart SFTP server
# ======================================================
if report_file and password:
    if st.button(
        "Configure Data & Upload to Instacart",
        use_container_width=True,
    ):
        output_folder = Path("temp_instacart_files")
        output_folder.mkdir(exist_ok=True)
        created_files = create_instacart_files(report_file, sales_file, output_folder, )
        uploaded = upload_files_to_instacart(created_files, password, )
        st.success(
            f"You have successfully uploaded {len(uploaded)} store files to Instacart."
        )
elif report_file:
    st.warning( # Warning for if the password is not entered when uploading!
        "Please enter the Instacart SFTP password before uploading."
    )
render_instacart_link() 
import streamlit as st
from pathlib import Path

from utils.instacart import create_instacart_files, upload_files_to_instacart


st.markdown("""
<div class="section-label">Instacart</div>
<div class="section-title">Instacart File Upload</div>
<div class="section-subtitle">
    Upload your Lightspeed report and sales file, then send the store files to Instacart.
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div style="text-align:center; margin-bottom:20px;">
    <a href="https://lightspeedanalytics.net/category/1/reports/99341"
       target="_blank"
       style="
            font-size:18px;
            font-weight:800;
            color:#C97822;
            text-decoration:none;
       ">
       Analytics Report →
    </a>
</div>
""", unsafe_allow_html=True)


report_file = st.file_uploader(
    "Upload Lightspeed Instacart Report",
    type=["csv"]
)

sales_file = st.file_uploader(
    "Upload Sales CSV",
    type=["csv"]
)

password = st.text_input(
    "Instacart SFTP Password",
    type="password"
)


if report_file and sales_file and password:
    st.caption(
        "Both files uploaded. Click below to create the store files and send them to Instacart."
    )

    if st.button("Create Files & Upload to Instacart", use_container_width=True):
        output_folder = Path("temp_instacart_files")
        output_folder.mkdir(exist_ok=True)

        created_files = create_instacart_files(
            report_file,
            sales_file,
            output_folder
        )

        uploaded = upload_files_to_instacart(created_files, password)

        st.success(f"Successfully uploaded {len(uploaded)} store files to Instacart.")


elif report_file and not sales_file:
    st.warning("Please upload the Sales CSV before sending files to Instacart.")

elif sales_file and not report_file:
    st.warning("Please upload the Lightspeed Instacart Report before sending files to Instacart.")
elif report_file and sales_file and not password:
    st.warning("Please enter the Instacart SFTP password before uploading.")

else:
    st.caption("Upload both CSV files to begin.")


st.markdown("""
<div style="text-align:center; margin-top:24px;">
    <a href="https://dashboard.instacart.com/partners/11797/warehouses/10587/reports/files"
       target="_blank"
       style="
            font-size:16px;
            font-weight:800;
            color:#1D5A3E;
            text-decoration:none;
       ">
       Open Instacart Uploads →
    </a>
</div>
""", unsafe_allow_html=True)
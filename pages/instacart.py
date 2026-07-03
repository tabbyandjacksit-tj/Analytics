import streamlit as st
from pathlib import Path

from utils.instacart import create_instacart_files, upload_files_to_instacart


PASSWORD = "Ella!"

if "instacart_authenticated" not in st.session_state:
    st.session_state.instacart_authenticated = False


@st.dialog("Need Access?")
def access_help():
    st.write("""
    This page is restricted to specific authorized employees. 

    If you need access or have any questions, please contact:
    **Maria Swenson** 
    """)


if not st.session_state.instacart_authenticated:
    password = st.text_input("Enter password to access this page", type="password")

    if st.button("Unlock", use_container_width=True):
        if password == PASSWORD:
            st.session_state.instacart_authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")

    if st.button("Need Access?", use_container_width=True):
        access_help()

    st.stop()

st.markdown("""
<style>

/* PAGE WIDTH */
.block-container {
    max-width: 1050px;
}

/* HEADINGS */
.section-label {
    color: #C97822;
    font-weight: 800;
    font-size: 13px;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.section-title {
    color: #1D5A3E;
    font-size: 31px;
    font-weight: 800;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #5C7A58;
    font-size: 16px;
    margin-bottom: 20px;
}

/* FILE UPLOADER */
section[data-testid="stFileUploader"] {
    background-color: #FFF9EF;
    padding: 22px;
    border-radius: 22px;
    border: 1px solid #D7C8A4;
    box-shadow: 0px 4px 14px rgba(47,55,45,0.07);
}

/* BUTTONS */
.stButton button {
    background-color: #1D5A3E;
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: 700;
}

.stButton button:hover {
    background-color: #15442F;
}

/* PASSWORD BOX */
div[data-testid="stTextInput"] input {
    background-color: #FFF9EF;
    border: 1px solid #D7C8A4;
    border-radius: 12px;
}

/* CAPTIONS */
[data-testid="stCaptionContainer"] {
    color: #5C7A58;
}

.report-help-card {
    background: #FFF9EF;
    border: 1px solid #D7C8A4;
    border-radius: 18px;
    padding: 18px 20px;
    margin: 22px 0 24px 0;
    box-shadow: 0px 4px 14px rgba(47,55,45,0.07);
}

.report-help-label {
    color: #C97822;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.report-help-title {
    color: #1D5A3E;
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 16px;
}

.report-help-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
}

.report-help-grid div {
    background: #F6EEDC;
    border-radius: 14px;
    padding: 14px 16px;
    color: #1D5A3E;
    font-weight: 700;
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 56px;
}

.report-help-check {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: #C97822;
    color: white;
    font-size: 14px;
    font-weight: bold;
    margin-right: 10px;
    flex-shrink: 0;
}

.report-help-footer {
    margin-top: 16px;
    color: #5C7A58;
    font-size: 15px;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="section-label">Instacart</div>
<div class="section-title">Instacart File Upload</div>
<div class="section-subtitle">
    Process your inventory report and send the generated store files to Instacart.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="report-help-card">
<div class="report-help-label">Required Report</div>
<div class="report-help-title">Inventory → Item Search</div>

<div class="report-help-grid">
<div>
<span class="report-help-check">✓</span>
<b>Check Show All Locations</b>
</div>

<div>
<span class="report-help-check">✓</span>
<b>Check Items w/ Inventory</b>
</div>

<div>
<span class="report-help-check">✓</span>
<b>Set Shop = All Shops</b>
</div>
</div>

<div class="report-help-footer">
After running the search, export the CSV and upload it below.
</div>
</div>
""", unsafe_allow_html=True)

report_file = st.file_uploader(
    label="Upload CSV Here",
    type=["csv"],
    label_visibility="collapsed"
)

password = st.text_input(
    "Enter Instacart SFTP Password",
    type="password"
)

sales_file = Path("utils/data/sales.csv")


if report_file and password:
    if st.button("Configure Data & Upload to Instacart", use_container_width=True):
        output_folder = Path("temp_instacart_files")
        output_folder.mkdir(exist_ok=True)

        created_files = create_instacart_files(
            report_file,
            sales_file,
            output_folder
        )

        uploaded = upload_files_to_instacart(created_files, password)

        st.success(f"Successfully uploaded all {len(uploaded)} store files to Instacart.")

elif report_file and not password:
    st.warning("Please enter the Instacart SFTP password before uploading.")

else:
    pass


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
       Access Instacart Uploads Here →
    </a>
</div>
""", unsafe_allow_html=True)
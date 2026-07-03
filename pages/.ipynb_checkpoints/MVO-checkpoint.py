import streamlit as st
import pandas as pd
import numpy as np
import base64
from datetime import datetime, timedelta


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


st.set_page_config(
    page_title="Major Vendor Order",
    page_icon="images/logo.png",
    layout="wide"
)


##############################################################################
#### Here sets all of the features to how this specific page appears. 
###  
### To see how the primary app appearances look, check out app.py
##############################################################################

st.markdown("""
<style>

/* HIDES STREAMLIT'S BUILT-IN ACCESSORIES */
footer {
    visibility: hidden;
}

[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none;
}


/* MAIN APPEARANCE */
.stApp {
    background-color: #F6F1E5; /* Sets the main background color */
    color: #2F372D; /* Sets the text color */
}

/* SETS THE SPACING AND WIDTH OF THE PAGE */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1050px;
}

/* HEADER APPEARANCE */
.hero {
    background-color: #1D5A3E;
    padding: 28px 28px;
    border-radius: 26px;
    margin-bottom: 28px;
    box-shadow: 0px 8px 22px rgba(29,90,62,.18);
}

/* TITLE APPEARANCE */
.hero h1 {
    text-align: center;
    color: #FFF9EF;
    font-size: 44px;
    font-weight: 800;
    margin: 0;
}

/* SUBTITLE APPEARANCE */
.hero p {
    text-align: center;
    color: rgba(255,249,239,0.88);
    font-size: 17px;
    margin-top: 12px;
    margin-bottom: 0;
}

/* ORANGE STEP LABEL APPEARANCE */
.section-label {
    color: #C97822;
    font-weight: 800;
    font-size: 13px;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

/* GREEN STEP HEADING APPEARANCE */
.section-title {
    color: #1D5A3E;
    font-size: 31px;
    font-weight: 800;
    margin-bottom: 4px;
}

/* SUBTITLE WITHIN STEP APPEARANCE */
.section-subtitle {
    color: #5C7A58;
    font-size: 16px;
    margin-bottom: 20px;
}

/* INSTRUCTION CARD'S APPEARANCE */
.mini-step {
    background-color: #FDF7EA;
    border: 1px solid #D7C8A4;
    border-radius: 18px;
    padding: 14px 10px;
    min-height: 115px;
    text-align: center;
    box-shadow: 0px 3px 10px rgba(47,55,45,0.04);
}

/* INSTRUCTION CARD NUMBER'S APPEARANCE */
.mini-number {
    background-color: #C97822;
    color: white;
    width: 28px;
    height: 28px;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 14px;
    margin-bottom: 6px;
}

/* INSTRUCTION CARD HEADING APPEARANCE */
.mini-step h4 {
    color: #1D5A3E;
    font-size: 16px;
    margin: 5px 0 3px 0;
}

/* INSTRUCTION CARD DESCRIPTION */
.mini-step p {
    color: #5C7A58;
    font-size: 12px;
    margin: 0;
    line-height: 1.35;
}

/* BUTTON APPEARANCE */
.stButton button {
    background-color: #C97822;
    color: white;
    border-radius: 12px;
    padding: 0.55rem 1rem;
    border: none;
    font-weight: 700;
}

/* BUTTON HOVER APPEARANCE */
.stButton button:hover {
    background-color: #B4671C;
    color: white;
}

/* DOWNLOAD BUTTON APPEARANCE */
.stDownloadButton button {
    background-color: #1D5A3E;
    color: white;
    border-radius: 12px;
    padding: 0.55rem 1rem;
    border: none;
    font-weight: 700;
}

/* DOWNLOAD BUTTON HOVER APPEARANCE */
.stDownloadButton button:hover {
    background-color: #15442F;
    color: white;
}

/* FILE UPLOAD APPEARANCE */
section[data-testid="stFileUploader"] {
    background-color: #FFF9EF;
    padding: 22px;
    border-radius: 22px;
    border: 1px solid #D7C8A4;
    box-shadow: 0px 4px 14px rgba(47,55,45,0.07);
}


/* DIVIDING LINE APPEARANCE */
hr {
    border: none;
    border-top: 1px solid #D7C8A4;
    margin: 2rem 0;
}

/* DATE INFO BOX */

/* DATE INFO CARD */
.date-card {
    background-color: #FDF7EA;
    border: 1px solid #D7C8A4;
    border-radius: 18px;
    padding: 10px 20px;
    margin-top: 15px;
    margin-bottom: 20px;
    box-shadow: 0px 3px 10px rgba(47,55,45,0.04);
}

.date-card-inner {
    display: flex;
    align-items: center;
    gap: 18px;
}

.date-icon {
    width: 46px;
    height: auto;
}

.date-title {
    color: #1D5A3E;
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 6px;
}

.date-text {
    color: #5C7A58;
    font-size: 14px;
    line-height: 1.6;
    margin: 0;
}

.date-text strong {
    color: #1D5A3E;
}

/* SETS HEADERS TO GREEN */
h2, h3 {
    color: #1D5A3E;
}
</style>
""", unsafe_allow_html=True)

##########################################################
### END OF MAIN APPEARANCE CSS 
##########################################################


logo = image_to_base64("images/logo.png")


# Written information for the title 
st.markdown("""
<div class="hero">
    <h1>Major Vendor Order Report</h1>
    <p>Generate a vendor order from a Lightspeed item sales report.</p>
</div>
""", unsafe_allow_html=True)


# Written information for step 1 (orange heading starts)  
st.markdown("""
<div class="section-label">Step 1</div>
<div class="section-title">Export Report from Lightspeed</div>
<div class="section-subtitle">Follow these steps to export the correct CSV report.</div>
""", unsafe_allow_html=True)

##############################################################################
#### This is where the code for the instruction cards and appearance lives 
###  other than the CSS 
### 
##############################################################################

steps = [ # Reads in the images for the step cards as well as set the titles for them! 
    ("images/reports.png", "Reports", "Open REPORTS from the sidebar."),
    ("images/grouped_sales.png", "Grouped Sales", "Scroll to GROUPED SALES TOTAL."),
    ("images/item_report.png", "Item Report", "Select ITEM as the report type."),
    ("images/calendar.png", "Date Filter", "Set DATE RANGE based on report frequency below."),
    ("images/vendor.png", "Vendor Filter", "Choose the desired VENDOR."),
    ("images/export.png", "Export CSV", "Press EXPORT and save the CSV.")
]


### This function reads in the image, title and description for each indivisual step. 
def render_instruction_card(number, image_path, title, desc):
    image = image_to_base64(image_path)

    # CSS for the the instruction card and how it looks aestetically 
    st.markdown(f"""
    <div class="mini-step">
        <div class="mini-number">{number}</div>
        <br>
        <img src="data:image/png;base64,{image}" width="42" style="margin:0 auto 5px auto;"> 
        <h4>{title}</h4>
        <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)



row1 = st.columns(3)
for i, step in enumerate(steps[:3]):
    with row1[i]:
        render_instruction_card(i + 1, *step)


st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)


row2 = st.columns(3)
for i, step in enumerate(steps[3:]):
    with row2[i]:
        render_instruction_card(i + 4, *step)


### Box for the date 56 days ago 
bi_report_start = datetime.today() - timedelta(days=56)
weekly_report_start = datetime.today() - timedelta(days=28)

calendar_icon = image_to_base64("images/calendar.png")

st.markdown(f"""
<div class="date-card">
<div class="date-card-inner">
<img src="data:image/png;base64,{calendar_icon}" class="date-icon">
<div>
<div class="date-title">Report Date Range</div>
<div class="date-text">
<strong>Bi-Weekly Orders:</strong> {bi_report_start.strftime("%B %d, %Y")}
<br>
<strong>Weekly Orders:</strong> {weekly_report_start.strftime("%B %d, %Y")}
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)


# Written information for step 2 
st.markdown("""
<div class="section-label">Step 2</div>
<div class="section-title">Upload Item Sale Report</div>
""", unsafe_allow_html=True)


uploaded_file = st.file_uploader( # Creates the file uploader button 
    "Upload Lightspeed CSV",
    type=["csv"],
    label_visibility="collapsed"
)


# Warning label for uploading the CSV 
st.caption("Please use only the CSV exported directly from Lightspeed. Do not edit or open file.")
st.divider()


if uploaded_file:
    # Read in file & make sure it is right file 
    df = pd.read_csv(uploaded_file)
    required_columns = ["Stock", "Sold"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error( f"It appears that you may have uploaded the wrong file! Your file must contain these columns: {', '.join(missing_columns)}"
        )

    else:
        df["Order Qty"] = np.where(
            (df["Stock"] <= 0) & (df["Sold"] == 1), # If QOH = 0 and total_quantity = 1,2 ... 
            2, # Than Order QTY = 2 
            np.where(
                # if(quantity_on_hand <= 0, total_quantity * (3/4), ...)
                df["Stock"] <= 0,
                df["Sold"] * (3 / 4),
                np.where(
                    # if(quantity_on_hand < 2, total_quantity / 2, ...)
                    df["Stock"] < 2,
                    df["Sold"] / 2,
                    np.where (
                        # if((total_quantity / 2) - quantity_on_hand < 0, 0, ...)
                        (df["Sold"] / 2) - df["Stock"] < 0,
                        0,
                        # else Order Qty = (Sold / 2) - Stock
                        (df["Sold"] / 2) - df["Stock"]
                    )
                )
            )
        )


        df["Order Qty"] = np.ceil(df["Order Qty"]) # Round up 
        df["Order Qty"] = np.maximum(0, df["Order Qty"]) # Ensures no negatives
        df["Order Qty"] = df["Order Qty"].astype(int) # Convert to nearest integer
        output_df = df[df["Order Qty"] > 0].copy() # Only keep rows > 0 OQ 
        output_df = output_df.sort_values("Order Qty", ascending=False) # Sort largest to smallest

        # Written informnation for step 3 
        st.markdown("""
        <div class="section-label">Step 3</div>
        <div class="section-title">Order Results</div>
        <div class="section-subtitle">Review the recommended order quantities below, and download your CSV.</div>
        """, unsafe_allow_html=True)
        
        # Creates the preview box for seeing the potential output 
        st.markdown(""" 
        <h3 style="
            color:#1D5A3E;
            font-size:24px;
            font-weight:800;
            margin-bottom:10px;
        ">
            Major Order Preview
        </h3>
        """, unsafe_allow_html=True)

        st.dataframe(output_df.head(50), use_container_width=True) # Just shows the top 50 rows at our width 

        full_csv = output_df.to_csv(index=False) # Creates a full csv of the output 

        upc_order_df = output_df[["UPC", "Order Qty"]].copy() # Creates a dataframe of just the UPC and Order QTY 
        upc_order_csv = upc_order_df.to_csv(index=False) # Puts that df into a csv

        @st.dialog("Heads up!")
        def order_template_warning(): # Puts a warning label for opening the file as to not change the UPC's or the QTY 
            st.write(
                "ⓘ **Heads up!** Please **do** **not** open this file. "
                "Instead, import it directly into a Lightspeed Purchase Order."
            )

            st.download_button( # Creates the buttons for downloading the CSV 
                label="Download Order Template",
                data=upc_order_csv,
                file_name="upc_order_template.csv",
                mime="text/csv",
                use_container_width=True
            )

        left, spacer, right = st.columns([2, 8, 2])

        with left:
            st.download_button( # Creates the button for dowloading the entire the WHOLE unedited CSV 
            label="Download Unedited CSV",
            data=full_csv,
            file_name="major_vendor_order_output.csv",
            mime="text/csv",
            use_container_width=True
        )
 
        with right:
            if st.button("Download Order Template", use_container_width=True): # Sets the button's locations
                order_template_warning()

        st.markdown(
            "ⓘ **Heads Up!** After importing into Lightspeed, remove any discontinued items and any items with a blank Vendor ID."
        )

else:
    pass
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st

from utils.images import image_to_base64
from utils.styling import apply_base_styles, apply_mvo_styles, render_hero, section_header, apply_extra_css

st.set_page_config(
    page_title="Major Vendor Order",
    page_icon="images/logo.png",
    layout="wide"
)

apply_base_styles()

apply_mvo_styles()



# Written information for the title 
render_hero(
    "Major Vendor Order Report",
    "Generate a vendor order from a Lightspeed item sales report.",
)


# Written information for step 1 (orange heading starts)  
section_header(
    "Step 1",
    "Export Report from Lightspeed",
    "Follow these steps to export the correct CSV report.",
)

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
section_header(
    "Step 2",
    "Upload Item Sale Report",
)


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
        section_header(
            "Step 3",
            "Order Results",
            "Review the recommended order quantities below, and download your CSV.",
        )
        
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
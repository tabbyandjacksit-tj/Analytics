# =======================================================================================
# Imports
# =======================================================================================
import streamlit as st
# =======================================================================================
# Page Configuration (sets title, icon, and layout of page)
# CSS Styles also imported/applied
# =======================================================================================
st.title(":material/link: Helpful Links")
st.write("Easy access to commonly used websites and tools at Tabby & Jack's!")
st.divider()
# =======================================================================================
# Inventory Schedule Link
# =======================================================================================
st.link_button(
     ":material/inventory_2: Inventory Schedule",
     "https://docs.google.com/spreadsheets/d/1xA57rmNrJncakYEKfHGBNdOwWs4yPEyrK3YzqTE4So8/edit?usp=sharing",
     use_container_width=True,
 )
st.divider()
# =======================================================================================
# MAP Compliant Brands Link
# =======================================================================================
st.link_button(
     ":material/inventory_2: MAP Compliant Brands",
     "https://docs.google.com/spreadsheets/d/1jEMzkdoDlyFqdYH0YjBy4yMfza1-8XrJOnkCzhg88xM/edit?usp=sharing",
     use_container_width=True,
 )
st.divider()
# =======================================================================================
# Vendor Contact Sheet Link
# =======================================================================================
st.link_button(
     ":material/inventory_2: Vendor Contact Sheet",
     "https://docs.google.com/spreadsheets/d/18dn2ojjVdkF8QU1qTURwm3GmqOR2-eYvIn2IjGpUg4k/edit?usp=sharing",
     use_container_width=True,
 )
st.divider()

st.link_button(
    ":material/folder: PFX Monthly Drive",
    "https://drive.google.com/drive/folders/1EEUKoQeqaDybe_YadJXtiMOrInhfdSfF",
    use_container_width=True,
)
'st.divider()'


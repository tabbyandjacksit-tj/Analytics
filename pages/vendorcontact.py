#  {forestGreen,6} =====================================================================
# Imports
# =======================================================================================
import pandas as pd
import streamlit as st
from utils.styling.base import apply_base_styles, render_hero
from utils.styling.vendor import apply_vendor_styles, render_edit_box
#  {yellowgreen,7} =====================================================================
# Page Configuration (sets title, icon, and layout of page)
# =======================================================================================
st.set_page_config(
    page_title="Vendor Contacts",
    page_icon="images/logo.png",
    layout="wide",
)
# {yellowgreen, 8} =======================================================================================
# Apply CSS Styles
# =======================================================================================
apply_base_styles()
apply_vendor_styles()
render_hero(
    "☏ Vendor Contacts",
    "Search for reps, emails, and expiration policies.",
)

# =======================================================================================
# Initialize variables for the google sheet & checkbox columns
# =======================================================================================
SHEET_ID = "18dn2ojjVdkF8QU1qTURwm3GmqOR2-eYvIn2IjGpUg4k"
GID = "980561560"
SHEET_EDIT_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "18dn2ojjVdkF8QU1qTURwm3GmqOR2-eYvIn2IjGpUg4k/edit?usp=sharing"
)
CHECKBOX_COLUMNS = [
    "Credit back?",
    "Replacements?",
    "Case-by-Case Basis?",
]

# =======================================================================================
# Loads in the vendor contacts from the google sheet as a df and refreshes every 60 seconds.
# =======================================================================================
@st.cache_data(ttl=60) # ttl sets the tick time/ how often it refreshes the cache, in seconds. 60 seconds = 1 minute. If complaints, lower
def load_contacts() -> pd.DataFrame:
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"
    df = pd.read_csv(url)
    df = df.dropna(how="all")
    df = df.fillna("")
    return df
df = load_contacts()

# =======================================================================================
# Creates the search bar function for the dataframe, and displays the filtered results in a table.
# =======================================================================================
st.markdown("### Search Vendor Contacts")
search = st.text_input(
    "Search",
    placeholder="Search by brand, vendor, email, phone, notes...",
    label_visibility="collapsed",
)
if search:
    mask = df.astype(str).apply(
        lambda row: row.str.contains(search, case=False, na=False).any(),
        axis=1,
    )
    filtered = df[mask].copy()
else:
    filtered = df.copy()
st.write(f"**Showing {len(filtered)} of {len(df)} vendors**")
for col in CHECKBOX_COLUMNS:
    if col in filtered.columns:
        filtered[col] = (
            filtered[col]
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["true", "yes", "1", "checked"])
        )
st.dataframe(
    filtered,
    hide_index=True,
    use_container_width=True,
    height=550,
    column_config={ # Set the column names and makes them checkboxes. 
        "Credit back?": st.column_config.CheckboxColumn("Credit back?"),
        "Replacements?": st.column_config.CheckboxColumn("Replacements?"),
        "Case-by-Case Basis?": st.column_config.CheckboxColumn("Case-by-Case?"),
    },
)
# =======================================================================================
# Creates a box with a link to the google sheet for editing the vendor contacts.
# Only people with access to that google sheet can actually click into it! 
# =======================================================================================
render_edit_box(SHEET_EDIT_URL)
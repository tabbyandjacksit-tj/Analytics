import streamlit as st
import pandas as pd

# ---------------------------------------------------
# Page
# ---------------------------------------------------

st.title("📞 Vendor Contacts")
st.caption(
    "Search vendor representatives, emails, phone numbers, and brand policies."
)

# ---------------------------------------------------
# Google Sheet
# ---------------------------------------------------

SHEET_ID = "18dn2ojjVdkF8QU1qTURwm3GmqOR2-eYvIn2IjGpUg4k"
GID = "980561560"


@st.cache_data(ttl=60)
def load_contacts():
    url = (
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
        f"/export?format=csv&gid={GID}"
    )

    df = pd.read_csv(url)
    df = df.dropna(how="all")
    df = df.fillna("")

    return df


df = load_contacts()

# ---------------------------------------------------
# Search
# ---------------------------------------------------

search = st.text_input(
    "🔍 Search",
    placeholder="Search by brand, vendor, email, phone, notes..."
)

filtered = df.copy()

if search:
    mask = filtered.astype(str).apply(
        lambda row: row.str.contains(search, case=False, na=False).any(),
        axis=1
    )

    filtered = filtered[mask]

# ---------------------------------------------------
# Quick Filters
# ---------------------------------------------------

st.markdown("##### Quick Filters")

c1, c2, c3, _ = st.columns([0.7, 0.8, 0.9, 5])

with c1:
    credit = st.checkbox("💵")

with c2:
    replace = st.checkbox("🔄")

with c3:
    case = st.checkbox("⚖️")

if credit and "Credit back?" in filtered.columns:
    filtered = filtered[filtered["Credit back?"] == True]

if replace and "Replacements?" in filtered.columns:
    filtered = filtered[filtered["Replacements?"] == True]

if case and "Case-by-Case Basis?" in filtered.columns:
    filtered = filtered[filtered["Case-by-Case Basis?"] == True]

# ---------------------------------------------------
# Results
# ---------------------------------------------------

st.write(f"**Showing {len(filtered)} of {len(df)} vendors**")

st.dataframe(
    filtered,
    hide_index=True,
    use_container_width=True,
    height=850,
    column_config={
        "Brand": st.column_config.TextColumn(
            "Brand",
            width="medium",
        ),

        "Email": st.column_config.TextColumn(
            "Email",
            width="large",
        ),

        "Phone Number": st.column_config.TextColumn(
            "Phone",
            width="medium",
        ),

        "Credit back?": st.column_config.CheckboxColumn(
            "💵",
            width="small",
            help="Provides credit for expired product",
        ),

        "Replacements?": st.column_config.CheckboxColumn(
            "🔄",
            width="small",
            help="Will replace expired product",
        ),

        "Case-by-Case Basis?": st.column_config.CheckboxColumn(
            "⚖️",
            width="small",
            help="Handled individually",
        ),

        "Other/Notes": st.column_config.TextColumn(
            "Notes",
            width="large",
        ),
    },
)
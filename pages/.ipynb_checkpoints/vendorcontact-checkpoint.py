import streamlit as st
import pandas as pd

st.title("📞 Vendor Contacts")
st.caption("Find vendor emails, contacts, and brand policies.")

# -----------------------
# Google Sheet Info
# -----------------------

SHEET_ID = "18dn2ojjVdkF8QU1qTURwm3GmqOR2-eYvIn2IjGpUg4k"
GID = "980561560"


# -----------------------
# Page Styling
# -----------------------

st.markdown(
    """
<style>
.vendor-card {
    background: rgba(255, 249, 239, 0.65);
    border: 1px solid rgba(92, 128, 103, 0.20);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
}

.big-label {
    font-size: 1.05rem;
    font-weight: 800;
    color: #1D5A3E;
    margin-bottom: 6px;
}

.small-muted {
    color: #777777;
    font-size: .9rem;
}
</style>
""",
    unsafe_allow_html=True
)


# -----------------------
# Load Google Sheet
# -----------------------

@st.cache_data(ttl=60)
def load_contacts():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"
    df = pd.read_csv(url)

    df = df.dropna(how="all")
    df = df.fillna("")

    return df


df = load_contacts()


# -----------------------
# Search Section
# -----------------------

st.markdown('<div class="vendor-card">', unsafe_allow_html=True)

st.markdown('<div class="big-label">Search Vendor Contacts</div>', unsafe_allow_html=True)

search = st.text_input(
    "Search",
    placeholder="🔍 Search brand, email, credit policy, notes...",
    label_visibility="collapsed"
)

st.markdown("</div>", unsafe_allow_html=True)


# -----------------------
# Filtering
# -----------------------

filtered = df.copy()

if search:
    mask = filtered.astype(str).apply(
        lambda row: row.str.contains(search, case=False, na=False).any(),
        axis=1
    )
    filtered = filtered[mask]


# Optional checkbox filters
filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    credit_only = st.checkbox("Only credit-back brands")

with filter_col2:
    replacement_only = st.checkbox("Only replacement brands")

with filter_col3:
    case_by_case_only = st.checkbox("Only case-by-case brands")


if "Credit back?" in filtered.columns and credit_only:
    filtered = filtered[filtered["Credit back?"].astype(str).str.lower().isin(["true", "yes", "1"])]

if "Replacements?" in filtered.columns and replacement_only:
    filtered = filtered[filtered["Replacements?"].astype(str).str.lower().isin(["true", "yes", "1"])]

if "Case-by-Case Basis?" in filtered.columns and case_by_case_only:
    filtered = filtered[filtered["Case-by-Case Basis?"].astype(str).str.lower().isin(["true", "yes", "1"])]


# -----------------------
# Metrics
# -----------------------

metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    st.metric("Total Brands", len(df))

with metric_col2:
    st.metric("Results Showing", len(filtered))


# -----------------------
# Display Table
# -----------------------

if filtered.empty:
    st.info("No vendor contacts matched your search.")
else:
    st.dataframe(
        filtered,
        hide_index=True,
        use_container_width=True,
        height=700,
        column_config={
            "Brand": st.column_config.TextColumn(
                "Brand",
                width="large"
            ),
            "Email": st.column_config.TextColumn(
                "Email",
                width="large"
            ),
            "Credit back?": st.column_config.CheckboxColumn(
                "Credit Back",
                width="medium"
            ),
            "Replacements?": st.column_config.CheckboxColumn(
                "Replacements",
                width="medium"
            ),
            "Case-by-Case Basis?": st.column_config.CheckboxColumn(
                "Case-by-Case",
                width="medium"
            ),
        }
    )
# =============================================================================
# Imports
# =============================================================================

import pandas as pd
import streamlit as st

from utils.styling.base import (
    apply_base_styles,
    render_hero,
)

from utils.components.headers import (
    render_section_header,
)

from utils.reporting.salesbyhour import (
    find_missing_columns,
    prepare_sales_hour_report,
    build_heatmap,
    create_heatmap,
)

# =============================================================================
# Page Setup
# =============================================================================

st.set_page_config(
    page_title="Sales by Hour",
    page_icon="images/logo.png",
    layout="wide",
)

apply_base_styles()

render_hero(
    "Sales by Hour",
    (
        "Visualize which days and hours are busiest using a "
        "transaction heatmap."
    ),
)

# =============================================================================
# Upload
# =============================================================================

render_section_header(
    label="Step 1",
    title="Upload Sales by Hour Report",
    subtitle=(
        "Upload the CSV exported from Lightspeed."
    ),
)

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"],
    label_visibility="collapsed",
)

if uploaded_file is None:
    st.stop()

# =============================================================================
# Read file
# =============================================================================

try:
    report_df = pd.read_csv(uploaded_file)

except Exception as error:
    st.error(error)
    st.stop()

missing = find_missing_columns(report_df)

if missing:

    st.error(
        "Missing required columns:\n\n"
        + ", ".join(missing)
    )

    st.stop()

df = prepare_sales_hour_report(report_df)

# =============================================================================
# Options
# =============================================================================

render_section_header(
    label="Step 2",
    title="Display Options",
)

mode = st.radio(
    "Show",

    [
        "Average Transactions",
        "Percent of Sales",
    ],

    horizontal=True,
)
heatmap_colors = {
    "💗 Pink & Purple": "RdPu",
    "💙 Ocean Blue": "Blues",
    "💚 Forest Green": "Greens",
    "🧡 Sunset": "YlOrRd",
    "💜 Purple": "Purples",
    "🌊 Teal": "BuGn",
}

if "heatmap_theme" not in st.session_state:
    st.session_state.heatmap_theme = "💗 Pink & Purple"


color_choice = st.selectbox(
    "🎨 Choose heatmap colors",
    list(heatmap_colors.keys()),
    index=list(heatmap_colors.keys()).index(
        st.session_state.heatmap_theme
    ),
)

st.session_state.heatmap_theme = color_choice


# =============================================================================
# Heatmap
# =============================================================================

heatmap = build_heatmap(
    df,
    mode,
)

render_section_header(
    label="Step 3",
    title="Sales by Hour Heatmap",
)

figure = create_heatmap(
    heatmap,
    mode,
    cmap=heatmap_colors[color_choice],
)

st.pyplot(
    figure,
    use_container_width=True,
)

# =============================================================================
# Table
# =============================================================================

with st.expander(
    "View underlying values"
):

    st.dataframe(
        heatmap.round(2),
        use_container_width=True,
    )
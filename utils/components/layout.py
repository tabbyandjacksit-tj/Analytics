# =============================================================================
# IMPORTS
# =============================================================================

import streamlit as st


# =============================================================================
# SPACING
# =============================================================================

def add_vertical_space(size: int = 16) -> None:
    """Add controlled vertical spacing."""

    st.markdown(
        f'<div style="height: {size}px;"></div>',
        unsafe_allow_html=True,
    )


# =============================================================================
# DIVIDER
# =============================================================================

def render_divider() -> None:
    """Render the standard page divider."""

    st.markdown("<hr>", unsafe_allow_html=True)
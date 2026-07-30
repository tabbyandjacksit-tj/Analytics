# =============================================================================
# IMPORTS
# =============================================================================

import streamlit as st
from collections.abc import Callable
from typing import Any

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



def render_card_grid(
    items: list[dict[str, Any]],
    render_card: Callable[..., None],
    columns: int = 2,
    gap: str = "large",
    row_spacing: int = 18,
) -> None:
    """Render dictionaries as cards in a responsive grid."""

    for start in range(0, len(items), columns):
        grid_columns = st.columns(
            columns,
            gap=gap,
        )

        row_items = items[start:start + columns]

        for column, item in zip(
            grid_columns,
            row_items,
        ):
            with column:
                key = (
                    "open_"
                    + item["title"]
                    .lower()
                    .replace(" ", "_")
                )

                render_card(
                    item,
                    key=key,
                )

        if row_spacing:
            st.markdown(
                f"<div style='height: {row_spacing}px;'></div>",
                unsafe_allow_html=True,
            )
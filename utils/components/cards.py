# =============================================================================
# IMPORTS
# =============================================================================

import html

import streamlit as st
from datetime import datetime, timedelta

from utils.tools.images import image_to_base64


# =============================================================================
# INFORMATION CARD
# =============================================================================

def render_info_card(
    title: str,
    description: str,
    label: str = "",
) -> None:
    """Render a general informational card."""

    safe_title = html.escape(str(title))
    safe_description = html.escape(str(description))
    safe_label = html.escape(str(label))

    label_html = (
        f'<div class="tj-card-label">{safe_label}</div>'
        if safe_label
        else ""
    )

    st.markdown(
        f"""
<div class="tj-info-card">
    {label_html}
    <div class="tj-card-title">{safe_title}</div>
    <div class="tj-card-description">{safe_description}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# METRIC CARD
# =============================================================================

def render_metric_card(
    label: str,
    value: str | int,
    description: str = "",
) -> None:
    """Render one important number or result."""

    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))
    safe_description = html.escape(str(description))

    description_html = (
        f'<div class="tj-metric-description">{safe_description}</div>'
        if safe_description
        else ""
    )

    st.markdown(
        f"""
<div class="tj-metric-card">
    <div class="tj-metric-label">{safe_label}</div>
    <div class="tj-metric-value">{safe_value}</div>
    {description_html}
</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# EMPTY CARD
# =============================================================================

def render_empty_card(
    title: str,
    description: str,
    icon: str = "📄",
) -> None:
    """Render an empty state before data or results exist."""

    safe_title = html.escape(str(title))
    safe_description = html.escape(str(description))
    safe_icon = html.escape(str(icon))

    st.markdown(
        f"""
<div class="tj-empty-card">
    <div class="tj-empty-icon">{safe_icon}</div>
    <div class="tj-empty-title">{safe_title}</div>
    <div class="tj-empty-description">{safe_description}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# NOTE CARD
# =============================================================================

def render_note_card(
    title: str,
    text: str,
) -> None:
    """Render a smaller note or reminder card."""

    safe_title = html.escape(str(title))
    safe_text = html.escape(str(text))

    st.markdown(
        f"""
<div class="tj-note-card">
    <div class="tj-note-title">{safe_title}</div>
    <div class="tj-note-text">{safe_text}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# DATE & UPLOAD CARD
# =============================================================================
def render_upload_date_card(
    *,
    upload_label: str = "Upload Report",
    file_types: list[str] | None = None,
    days_label: str = "Number of Days",
    default_days: int = 90,
    min_days: int = 1,
    start_label: str = "Start Report",
    column_widths: tuple[float, float] = (3.2, 1),
):
    """
    Renders a reusable upload + date helper card.

    Returns:
        uploaded_file
        days_ago
        calculated_date
    """

    if file_types is None:
        file_types = ["csv"]

    with st.container(border=True):
        upload_col, date_col = st.columns(
            column_widths,
            vertical_alignment="top",
        )

        with upload_col:
            st.markdown(
                '<div class="tj-helper-label">Report File</div>',
                unsafe_allow_html=True,
            )

            uploaded_file = st.file_uploader(
                upload_label,
                type=file_types,
                label_visibility="collapsed",
            )

        with date_col:
            days_ago = st.number_input(
                days_label,
                min_value=min_days,
                value=default_days,
                step=1,
            )

            calculated_date = (
                datetime.today() - timedelta(days=days_ago)
            )

            st.markdown(
                f"""
                <div class="tj-date-result">
                    <span class="tj-date-result-label">
                        {start_label}:
                    </span>
                    <span class="tj-date-result-value">
                        {calculated_date:%B %d, %Y}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    return uploaded_file, days_ago, calculated_date

import streamlit as st


# =============================================================================
# INSTRUCTION CARD STYLES
# =============================================================================

def apply_instruction_styles() -> None:
    """Apply styling for reusable instruction cards."""

    st.markdown(
        """
        <style>
        /* your CSS here */
        </style>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# INSTRUCTION CARD
# =============================================================================

def render_instruction_card(
    number: int,
    title: str,
    description: str,
    image_path: str,
) -> None:
    """Render a reusable instruction card with an image."""

    safe_title = html.escape(str(title))
    safe_description = html.escape(str(description))

    image_base64 = image_to_base64(image_path)

    st.markdown(
        f"""
<div class="instruction-card">

    <div class="instruction-number">
        {number}
    </div>

    <div class="instruction-image-wrap">
        <img
            src="data:image/png;base64,{image_base64}"
            class="instruction-image"
        >
    </div>

    <div class="instruction-title">
        {safe_title}
    </div>

    <div class="instruction-description">
        {safe_description}
    </div>

</div>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# INSTRUCTION GRID
# =============================================================================

def render_instruction_grid(
    steps,
    columns_per_row: int = 3,
    row_gap: int = 18,
):
    """Render instruction cards in a grid."""

    for row_start in range(
        0,
        len(steps),
        columns_per_row,
    ):
        row_steps = steps[
            row_start:row_start + columns_per_row
        ]

        columns = st.columns(
            columns_per_row,
            gap="medium",
        )

        for offset, step in enumerate(row_steps):
            with columns[offset]:
                render_instruction_card(
                    row_start + offset + 1,
                    *step,
                )

        if row_start + columns_per_row < len(steps):
            st.markdown(
                f"<div style='height:{row_gap}px'></div>",
                unsafe_allow_html=True,
            )
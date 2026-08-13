from __future__ import annotations
import html

import base64
from datetime import datetime, timedelta
from pathlib import Path
import streamlit as st


# =============================================================================
# Image Helper
# =============================================================================
def _image_to_base64(image_path: str) -> str:
    """
    Convert an image file to a base64 data URI.
    """
    path = Path(image_path)

    if not path.exists():
        return ""

    suffix = path.suffix.lower()

    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
    }

    mime_type = mime_types.get(
        suffix,
        "application/octet-stream",
    )

    encoded = base64.b64encode(
        path.read_bytes()
    ).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"


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
    safe_number = html.escape(str(number))

    image_data = _image_to_base64(image_path)

    if image_data:
        image_html = (
            '<div class="instruction-image-wrapper">'
            f'<img src="{image_data}" '
            f'alt="{safe_title}" '
            'class="instruction-image">'
            '</div>'
        )
    else:
        image_html = ""

    card_html = (
        '<div class="instruction-card">'
        f'<div class="instruction-number">{safe_number}</div>'
        f'{image_html}'
        f'<div class="instruction-title">{safe_title}</div>'
        f'<div class="instruction-description">{safe_description}</div>'
        '</div>'
    )

    st.markdown(
        card_html,
        unsafe_allow_html=True,
    )
# =============================================================================
# Instruction Grid
# =============================================================================
# =============================================================================
# INSTRUCTION GRID
# =============================================================================

def render_instruction_grid(
    steps,
    columns_per_row: int = 3,
    row_gap: int = 18,
):
    """
    Render instruction cards in rows.

    Supports:
    - tuples/lists containing:
        (title, description, image_path)

    - dictionaries containing:
        title, description, image_path

    Step numbers are generated automatically.
    """

    for start in range(0, len(steps), columns_per_row):
        row_steps = steps[
            start:start + columns_per_row
        ]

        columns = st.columns(
            len(row_steps)
        )

        for offset, (column, step) in enumerate(
            zip(columns, row_steps)
        ):
            step_number = start + offset + 1

            with column:

                # Dictionary-style step
                if isinstance(step, dict):
                    render_instruction_card(
                        number=step.get(
                            "number",
                            step_number,
                        ),
                        title=step["title"],
                        description=step["description"],
                        image_path=step["image_path"],
                    )

                # Tuple/list-style step
                else:
                    title, description, image_path = step

                    render_instruction_card(
                        number=step_number,
                        title=title,
                        description=description,
                        image_path=image_path,
                    )

        # Add spacing between rows
        if start + columns_per_row < len(steps):
            st.markdown(
                f"""
                <div style="height:{row_gap}px;"></div>
                """,
                unsafe_allow_html=True,
            )

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
    Render a reusable upload + date helper card.

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
                datetime.today()
                - timedelta(days=days_ago)
            )

            date_html = (
                '<div class="tj-date-result">'
                f'<span class="tj-date-result-label">'
                f'{html.escape(str(start_label))} : '
                f'</span>'
                f'<span class="tj-date-result-value">'
                f'{calculated_date:%B %d, %Y}'
                f'</span>'
                '</div>'
            )

            st.markdown(
                date_html,
                unsafe_allow_html=True,
            )

    return uploaded_file, days_ago, calculated_date
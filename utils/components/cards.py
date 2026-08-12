from __future__ import annotations

import base64
import textwrap
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
# Instruction Card
# =============================================================================
def render_instruction_card(
    number: int,
    title: str,
    description: str,
    image_path: str | None = None,
) -> None:
    """
    Render one instruction card.
    """

    image_html = ""

    if image_path:
        image_data = _image_to_base64(image_path)

        if image_data:
            image_html = f"""
            <div class="instruction-image-wrapper">
                <img
                    src="{image_data}"
                    class="instruction-image"
                    alt="{title}"
                >
            </div>
            """

    card_html = f"""
    <div class="instruction-card">

        <div class="instruction-number">
            {number}
        </div>

        {image_html}

        <div class="instruction-title">
            {title}
        </div>

        <div class="instruction-description">
            {description}
        </div>

    </div>
    """

    st.markdown(
        textwrap.dedent(card_html),
        unsafe_allow_html=True,
    )


# =============================================================================
# Instruction Grid
# =============================================================================
def render_instruction_grid(
    steps: list[dict],
    columns_per_row: int = 3,
    row_gap: int = 18,
) -> None:
    """
    Render instruction cards in rows.
    """

    for row_start in range(
        0,
        len(steps),
        columns_per_row,
    ):
        row_steps = steps[
            row_start:row_start + columns_per_row
        ]

        columns = st.columns(
            len(row_steps),
            gap="medium",
        )

        for column, step in zip(
            columns,
            row_steps,
        ):
            with column:
                render_instruction_card(
                    number=step["number"],
                    title=step["title"],
                    description=step["description"],
                    image_path=step.get("image"),
                )

        if (
            row_start + columns_per_row
            < len(steps)
        ):
            st.markdown(
                f"<div style='height:{row_gap}px'></div>",
                unsafe_allow_html=True,
            )
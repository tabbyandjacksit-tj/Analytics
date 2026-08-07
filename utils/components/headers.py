# =============================================================================
# IMPORTS
# =============================================================================

import html

import streamlit as st


# =============================================================================
# STANDARD SECTION HEADER
# =============================================================================

def render_section_header(
    title: str,
    subtitle: str = "",
    label: str = "",
    hide_label: bool = False,
) -> None:
    """Render a standard section heading."""

    safe_title = html.escape(str(title))
    safe_subtitle = html.escape(str(subtitle))
    safe_label = html.escape(str(label))

    label_html = (
        f'<div class="tj-section-label">{safe_label}</div>'
        if safe_label and not hide_label
        else ""
    )

    subtitle_html = (
        f'<div class="tj-section-subtitle">{safe_subtitle}</div>'
        if safe_subtitle
        else ""
    )

    st.markdown(
        f"""
        <div class="tj-section-header">
            {label_html}
            <div class="tj-section-title">{safe_title}</div>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# SMALLER SUBSECTION HEADER
# =============================================================================

def render_subsection_header(
    title: str,
    subtitle: str = "",
) -> None:
    """Render a smaller heading within a page section."""

    safe_title = html.escape(str(title))
    safe_subtitle = html.escape(str(subtitle))

    subtitle_html = (
        f'<div class="tj-subsection-subtitle">{safe_subtitle}</div>'
        if safe_subtitle
        else ""
    )

    st.markdown(
        f"""
        <div class="tj-subsection-header">
            <div class="tj-subsection-title">{safe_title}</div>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
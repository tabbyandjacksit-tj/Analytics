import html

import streamlit as st


def render_section_header(
    title: str,
    subtitle: str = "",
    eyebrow: str = "",
) -> None:
    """Render a standard page-section heading."""

    safe_title = html.escape(str(title))
    safe_subtitle = html.escape(str(subtitle))
    safe_eyebrow = html.escape(str(eyebrow))

    eyebrow_html = (
        f'<div class="tj-eyebrow">{safe_eyebrow}</div>'
        if safe_eyebrow
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
    {eyebrow_html}
    <div class="tj-section-title">{safe_title}</div>
    {subtitle_html}
</div>
""",
        unsafe_allow_html=True,
    )
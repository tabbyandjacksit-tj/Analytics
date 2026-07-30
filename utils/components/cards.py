# =============================================================================
# IMPORTS
# =============================================================================

import html

import streamlit as st


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
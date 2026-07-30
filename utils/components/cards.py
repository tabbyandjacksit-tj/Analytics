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
    """
    Render a general informational card.

    Parameters
    ----------
    title:
        Main card heading.

    description:
        Supporting card text.

    label:
        Optional small uppercase label displayed above the title.
    """

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
    """
    Render a card displaying one important number or value.

    Parameters
    ----------
    label:
        Small heading describing the value.

    value:
        Main value shown prominently.

    description:
        Optional supporting information.
    """

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
# EMPTY STATE CARD
# =============================================================================

def render_empty_state(
    title: str,
    description: str,
    icon: str = "📄",
) -> None:
    """
    Render a placeholder when no content or results are available.

    Parameters
    ----------
    title:
        Main empty-state message.

    description:
        Instructions explaining what the user should do next.

    icon:
        Optional emoji or symbol displayed above the title.
    """

    safe_title = html.escape(str(title))
    safe_description = html.escape(str(description))
    safe_icon = html.escape(str(icon))

    st.markdown(
        f"""
<div class="tj-empty-state">
    <div class="tj-empty-icon">{safe_icon}</div>
    <div class="tj-empty-title">{safe_title}</div>
    <div class="tj-empty-description">{safe_description}</div>
</div>
""",
        unsafe_allow_html=True,
    )
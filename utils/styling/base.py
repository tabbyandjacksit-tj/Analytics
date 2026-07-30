# =============================================================================
# IMPORTS
# =============================================================================

import html

import streamlit as st


# =============================================================================
# EXTRA CSS
# =============================================================================

def apply_extra_css(css: str) -> None:
    """Apply additional CSS to the current Streamlit page."""

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )


# =============================================================================
# BASE STYLES
# =============================================================================

def apply_base_styles(max_width: int = 1050) -> None:
    """Apply shared site-wide styles."""

    st.markdown(
        f"""
<style>
/* ==========================================================================
   STREAMLIT PAGE
   ========================================================================== */

footer {{
    visibility: hidden;
}}

[data-testid="stToolbar"],
[data-testid="stDecoration"] {{
    display: none;
}}

.stApp {{
    background-color: #F6F1E5;
    color: #2F372D;
}}

.block-container {{
    max-width: {max_width}px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}}


/* ==========================================================================
   FORM INPUTS
   ========================================================================== */

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextArea"] textarea {{
    background-color: #FFF9EF;
    border: 1px solid #D7C8A4;
    border-radius: 12px;
    color: #2F372D;
}}

section[data-testid="stFileUploader"] {{
    background-color: #FFF9EF;
    border: 1px solid #D7C8A4;
    border-radius: 22px;
    box-shadow: 0 4px 14px rgba(47, 55, 45, 0.07);
    padding: 22px;
}}


/* ==========================================================================
   STANDARD BUTTONS
   ========================================================================== */

.stButton button {{
    background-color: #1D5A3E;
    border: none;
    border-radius: 12px;
    color: white;
    font-weight: 700;
}}

.stButton button:hover {{
    background-color: #15442F;
    color: white;
}}

.stDownloadButton button {{
    background-color: #C97822;
    border: none;
    border-radius: 12px;
    color: white;
    font-weight: 700;
}}

.stDownloadButton button:hover {{
    background-color: #B4671C;
    color: white;
}}

.stLinkButton a {{
    background-color: #1D5A3E;
    border-radius: 12px;
    color: white;
    font-weight: 700;
}}

.stLinkButton a:hover {{
    background-color: #15442F;
    color: white;
}}


/* ==========================================================================
   OTHER STREAMLIT ELEMENTS
   ========================================================================== */

[data-testid="stCaptionContainer"] {{
    color: #5C7A58;
}}

hr {{
    border: none;
    border-top: 1px solid #D7C8A4;
    margin: 2rem 0;
}}
</style>
""",
        unsafe_allow_html=True,
    )


# =============================================================================
# HERO
# =============================================================================

def render_hero(
    title: str,
    subtitle: str,
) -> None:
    """Render the standard centered page hero."""

    safe_title = html.escape(str(title))
    safe_subtitle = html.escape(str(subtitle))

    st.markdown(
        f"""
<div class="tj-hero">
    <h1>{safe_title}</h1>
    <p>{safe_subtitle}</p>
</div>
""",
        unsafe_allow_html=True,
    )
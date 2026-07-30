import streamlit as st


def apply_extra_css(css: str) -> None:
    """Apply an additional block of CSS to the current Streamlit page."""

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )


def apply_base_styles(max_width: int = 1050) -> None:
    """Apply global Tabby & Jack's design-system styles."""

    st.markdown(
        f"""
<style>
/* ==========================================================================
   DESIGN TOKENS
   ========================================================================== */

:root {{
    --tj-green-900: #0F3324;
    --tj-green-700: #15442F;
    --tj-green-600: #1D5A3E;
    --tj-green-400: #5C8067;
    --tj-green-muted: #5C7A58;
    --tj-green-soft: #EAF5EE;

    --tj-orange-600: #C97822;
    --tj-orange-500: #EF8B1D;
    --tj-orange-soft: #FFF2DF;

    --tj-cream-100: #FFFDF8;
    --tj-cream-200: #FFF9EF;
    --tj-beige-100: #FDF7EA;
    --tj-beige-200: #F6F1E5;

    --tj-text: #2F372D;
    --tj-text-muted: #5C7A58;
    --tj-text-disabled: #7B776E;

    --tj-border: #D7C8A4;
    --tj-border-soft: #E6DECE;

    --tj-success: #1D8A45;
    --tj-success-soft: #E6F5EC;
    --tj-warning-soft: #FFF2DF;
    --tj-danger: #B94A48;
    --tj-danger-soft: #FBE9E8;

    --tj-radius-sm: 12px;
    --tj-radius-md: 18px;
    --tj-radius-lg: 22px;
    --tj-radius-xl: 26px;

    --tj-shadow-sm: 0 3px 10px rgba(47, 55, 45, 0.04);
    --tj-shadow-md: 0 6px 18px rgba(47, 55, 45, 0.08);
    --tj-shadow-lg: 0 10px 28px rgba(29, 90, 62, 0.14);
}}

/* ==========================================================================
   STREAMLIT SHELL
   ========================================================================== */

footer {{
    visibility: hidden;
}}

[data-testid="stToolbar"],
[data-testid="stDecoration"] {{
    display: none;
}}

.stApp {{
    background-color: var(--tj-beige-200);
    color: var(--tj-text);
}}

.block-container {{
    max-width: {max_width}px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}}

/* ==========================================================================
   TYPOGRAPHY
   ========================================================================== */

.tj-eyebrow {{
    color: var(--tj-orange-600);
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    margin: 0 0 5px;
    text-transform: uppercase;
}}

.tj-section-title {{
    color: var(--tj-green-600);
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.2;
    margin: 0;
}}

.tj-section-subtitle {{
    color: var(--tj-text-muted);
    font-size: 1rem;
    line-height: 1.5;
    margin: 7px 0 20px;
}}

.tj-card-title {{
    color: var(--tj-green-600);
    font-size: 1.2rem;
    font-weight: 800;
    line-height: 1.3;
    margin: 0;
}}

.tj-helper-text {{
    color: var(--tj-text-muted);
    font-size: 0.9rem;
    line-height: 1.5;
}}

/* ==========================================================================
   FORM CONTROLS
   ========================================================================== */

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextArea"] textarea {{
    background-color: var(--tj-cream-200);
    border: 1px solid var(--tj-border);
    border-radius: var(--tj-radius-sm);
    color: var(--tj-text);
}}

section[data-testid="stFileUploader"] {{
    background-color: var(--tj-cream-200);
    border: 1px solid var(--tj-border);
    border-radius: var(--tj-radius-lg);
    box-shadow: var(--tj-shadow-sm);
    padding: 22px;
}}

/* ==========================================================================
   PRIMARY BUTTONS
   ========================================================================== */

.stButton button {{
    background-color: var(--tj-green-600);
    border: 1px solid var(--tj-green-600);
    border-radius: var(--tj-radius-sm);
    color: white;
    font-weight: 700;
}}

.stButton button:hover {{
    background-color: var(--tj-green-700);
    border-color: var(--tj-green-700);
    color: white;
}}

/* ==========================================================================
   DOWNLOAD BUTTONS
   ========================================================================== */

.stDownloadButton button {{
    background-color: var(--tj-orange-600);
    border: 1px solid var(--tj-orange-600);
    border-radius: var(--tj-radius-sm);
    color: white;
    font-weight: 700;
}}

.stDownloadButton button:hover {{
    background-color: #B4671C;
    border-color: #B4671C;
    color: white;
}}

/* ==========================================================================
   LINK BUTTONS
   ========================================================================== */

.stLinkButton a {{
    background-color: var(--tj-green-600);
    border-radius: var(--tj-radius-sm);
    color: white;
    font-weight: 700;
}}

.stLinkButton a:hover {{
    background-color: var(--tj-green-700);
    color: white;
}}

/* ==========================================================================
   DIVIDERS AND CAPTIONS
   ========================================================================== */

hr {{
    border: none;
    border-top: 1px solid var(--tj-border);
    margin: 2rem 0;
}}

[data-testid="stCaptionContainer"] {{
    color: var(--tj-text-muted);
}}

/* ==========================================================================
   RESPONSIVE TYPOGRAPHY
   ========================================================================== */

@media (max-width: 750px) {{
    .tj-section-title {{
        font-size: 1.65rem;
    }}
}}
</style>
""",
        unsafe_allow_html=True,
    )
import streamlit as st

def apply_extra_css(css: str) -> None:
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def apply_base_styles(max_width: int = 1050) -> None:
    st.markdown(
        f"""
<style>
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
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: {max_width}px;
}}

.hero {{
    background-color: #1D5A3E;
    padding: 28px 28px;
    border-radius: 26px;
    margin-bottom: 28px;
    box-shadow: 0px 8px 22px rgba(29,90,62,.18);
}}

.hero h1 {{
    text-align: center;
    color: #FFF9EF;
    font-size: 44px;
    font-weight: 800;
    margin: 0;
}}

.hero p {{
    text-align: center;
    color: rgba(255,249,239,0.88);
    font-size: 17px;
    margin-top: 12px;
    margin-bottom: 0;
}}

h3 {{
    color: #1D5A3E;
    font-size: 28px;
    font-weight: 800;
}}

div[data-testid="stTextInput"] input {{
    background-color: #FFF9EF;
    border: 1px solid #D7C8A4;
    border-radius: 12px;
    color: #2F372D;
}}

.stLinkButton a {{
    background-color: #1D5A3E;
    color: white;
    border-radius: 12px;
    font-weight: 700;
}}

.stLinkButton a:hover {{
    background-color: #15442F;
    color: white;
}}
</style>
""",
        unsafe_allow_html=True,
    )


def render_hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
<div class="hero">
    <h1>{title}</h1>
    <p>{subtitle}</p>
</div>
""",
        unsafe_allow_html=True,
    )
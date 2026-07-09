import streamlit as st

from utils.images import image_to_base64
from utils.styling.base import apply_extra_css


def apply_mvo_styles() -> None:
    apply_extra_css(
        """
.section-label {
    color: #C97822;
    font-size: 14px;
    font-weight: 800;
    margin-top: 24px;
    margin-bottom: 4px;
}

.section-title {
    color: #1D5A3E;
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #2F372D;
    font-size: 15px;
    margin-bottom: 14px;
}

.mini-step {
    background-color: #FDF7EA;
    border: 1px solid #D7C8A4;
    border-radius: 18px;
    padding: 14px 10px;
    min-height: 115px;
    text-align: center;
    box-shadow: 0px 3px 10px rgba(47,55,45,0.04);
}

.mini-number {
    background-color: #C97822;
    color: white;
    width: 28px;
    height: 28px;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 14px;
    margin-bottom: 6px;
}

.mini-step h4 {
    color: #1D5A3E;
    font-size: 16px;
    margin: 5px 0 3px 0;
}

.mini-step p {
    color: #5C7A58;
    font-size: 12px;
    margin: 0;
    line-height: 1.35;
}

.stButton button {
    background-color: #C97822;
    color: white;
    border-radius: 12px;
    padding: 0.55rem 1rem;
    border: none;
    font-weight: 700;
}

.stButton button:hover {
    background-color: #B4671C;
    color: white;
}

.stDownloadButton button {
    background-color: #1D5A3E;
    color: white;
    border-radius: 12px;
    padding: 0.55rem 1rem;
    border: none;
    font-weight: 700;
}

.stDownloadButton button:hover {
    background-color: #15442F;
    color: white;
}

section[data-testid="stFileUploader"] {
    background-color: #FFF9EF;
    padding: 22px;
    border-radius: 22px;
    border: 1px solid #D7C8A4;
    box-shadow: 0px 4px 14px rgba(47,55,45,0.07);
}

hr {
    border: none;
    border-top: 1px solid #D7C8A4;
    margin: 2rem 0;
}

.date-card {
    background-color: #FDF7EA;
    border: 1px solid #D7C8A4;
    border-radius: 18px;
    padding: 10px 20px;
    margin-top: 15px;
    margin-bottom: 20px;
    box-shadow: 0px 3px 10px rgba(47,55,45,0.04);
}

.date-card-inner {
    display: flex;
    align-items: center;
    gap: 18px;
}

.date-icon {
    width: 46px;
    height: auto;
}

.date-title {
    color: #1D5A3E;
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 6px;
}

.date-text {
    color: #5C7A58;
    font-size: 14px;
    line-height: 1.6;
    margin: 0;
}

.date-text strong {
    color: #1D5A3E;
}
"""
    )


def section_header(label: str, title: str, subtitle: str = "") -> None:
    st.markdown(
        f"""
<div class="section-label">{label}</div>
<div class="section-title">{title}</div>
<div class="section-subtitle">{subtitle}</div>
""",
        unsafe_allow_html=True,
    )


def render_instruction_card(number: int, image_path: str, title: str, desc: str) -> None:
    image = image_to_base64(image_path)

    st.markdown(
        f"""
<div class="mini-step">
    <div class="mini-number">{number}</div>
    <br>
    <img src="data:image/png;base64,{image}" width="42" style="margin:0 auto 5px auto;">
    <h4>{title}</h4>
    <p>{desc}</p>
</div>
""",
        unsafe_allow_html=True,
    )
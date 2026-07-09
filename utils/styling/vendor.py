import streamlit as st

from utils.styling.base import apply_extra_css


def apply_vendor_styles() -> None:
    apply_extra_css(
        """
.edit-box {
    margin-top: 1.5rem;
    padding: 18px 22px;
    background-color: #FDF7EA;
    border: 1px solid #D7C8A4;
    border-radius: 18px;
    box-shadow: 0px 3px 10px rgba(47,55,45,0.04);
}

.edit-box h4 {
    margin: 0 0 .4rem 0;
    color: #1D5A3E;
}

.edit-box p {
    margin: 0;
    color: #5C7A58;
}

.edit-box a {
    color: #1D5A3E;
    font-weight: 800;
    text-decoration: none;
}
"""
    )


def render_edit_box(sheet_url: str) -> None:
    st.markdown(
        f"""
<div class="edit-box">
    <h4>✎ Looking to add or update a vendor contact?</h4>
    <p>
        This page is search-only.
        <a href="{sheet_url}" target="_blank">
            Click here to edit the Vendor Contact Sheet.
        </a>
    </p>
</div>
""",
        unsafe_allow_html=True,
    )


def section_header(label: str, title: str, subtitle: str = "") -> None:
    st.markdown(
        f"""
<div class="section-title">{title}</div>
<div class="section-subtitle">{subtitle}</div>
""",
        unsafe_allow_html=True,
    )
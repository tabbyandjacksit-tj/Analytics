import streamlit as st
import base64
from utils.images import image_to_base64


logo = image_to_base64("images/logo.png")

icons = {
    "ordering": image_to_base64("images/ordering.png"),
    "transfer": image_to_base64("images/item_report.png"),
    "small": image_to_base64("images/small_order.png"),
    "brand": image_to_base64("images/brand.png"),
}


tools = [
    {
        "title": "Major Vendor Order",
        "description": "Upload a 4-week Lightspeed report and generate a major vendor order.",
        "status": "Available",
        "category": "Ordering Tools",
        "icon": icons["ordering"],
        "page": "pages/MVO.py",
        "enabled": True,
    },
    {
        "title": "Small Vendor Order",
        "description": "Upload a 90-day Lightspeed report and generate a small vendor report.",
        "status": "Available",
        "category": "Ordering Tools",
        "icon": icons["small"],
        "page": "pages/SVO.py",
        "enabled": True,
    },
    {
        "title": "Dusty Report Transfer",
        "description": "Transfer Dusty inventory to the stores that need it most.",
        "status": "Coming Soon",
        "category": "Inventory Tools",
        "icon": icons["transfer"],
        "page": "pages/dusty.py",
        "enabled": False,
    },
    {
        "title": "Sales by Brand",
        "description": "Generate sales report based on brand and time frame.",
        "status": "Coming Soon",
        "category": "Inventory Tools",
        "icon": icons["brand"],
        "page": "pages/brandsale.py",
        "enabled": False,
    },
    {
        "title": "Vendor Contact Sheet",
        "description": "Link to Google Sheet containing information about how to contact vendors/reps.",
        "status": "Available",
        "category": "Office Hour Tools",
        "icon": icons["brand"],
        "page": "pages/vendorcontact.py",
        "enabled": True,
    },
    {
        "title": "Office Hour Tracker",
        "description": "Exclusively for work-from-home employees to track their working office hours.",
        "status": "Coming Soon",
        "category": "Office Hour Tools",
        "icon": icons["brand"],
        "page": None,
        "enabled": False,
    },
]


st.markdown(
    """
<style>
footer {
    visibility: hidden;
}


[data-testid="stDecoration"] {
    display: none;
}

.stApp {
    background-color: #F6F1E5;
    color: #2F372D;
}

.block-container {
    max-width: 1160px;
    padding-top: 1.25rem;
    padding-bottom: 3rem;
}


.app-banner {
    background: linear-gradient(135deg, #1D5A3E, #0F3324);
    border-radius: 22px;
    padding: 24px 34px;
    margin-bottom: 30px;
    min-height: 165px;
    display: flex;
    align-items: center;
    gap: 28px;
    box-shadow: 0px 12px 30px rgba(29,90,62,.22);
}

.banner-logo {
    background: rgba(255,249,239,.10);
    border: 1px solid rgba(255,249,239,.18);
    border-radius: 22px;
    padding: 16px;
}

.banner-title h1 {
    color: #FFF9EF;
    font-size: 42px;
    font-weight: 850;
    margin: 0;
}

.banner-title p {
    color: rgba(255,249,239,.88);
    font-size: 17px;
    margin: 10px 0 0 0;
}

.section-kicker {
    color: #EF8B1D;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    font-weight: 850;
    margin-bottom: 4px;
}

.section-title {
    color: #1D5A3E;
    font-size: 34px;
    font-weight: 850;
    margin-bottom: 3px;
}

.section-subtitle {
    color: #5C7A58;
    font-size: 16px;
    margin-bottom: 10px;
}

.category-title {
    color: #1D5A3E;
    font-size: 22px;
    font-weight: 850;
    margin: 10px 0 12px 0;
}

.app-card {
    background-color: #FFFDF8;
    border: 1px solid #D7C8A4;
    border-radius: 24px 24px 0 0;
    min-height: 220px;
    box-shadow: 0px 7px 22px rgba(47,55,45,.08);
    position: relative;
    overflow: hidden;
    transition: all .18s ease;
}

.app-card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 14px 34px rgba(29,90,62,.16);
    border-color: #EF8B1D;
}

.app-card::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 6px;
    background: #EF8B1D;
}

.app-card-body {
    padding: 30px;
    text-align: left;
}

.app-card-top {
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 22px;
}

.app-icon-wrap {
    background-color: #F6F1E5;
    width: 76px;
    height: 76px;
    border-radius: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.app-card h3 {
    color: #1D5A3E;
    font-size: 24px;
    font-weight: 850;
    margin: 0;
}

.status-pill {
    display: inline-block;
    margin-top: 8px;
    border-radius: 999px;
    padding: 5px 10px;
    font-size: 12px;
    font-weight: 800;
}

.status-available {
    background: #E6F5EC;
    color: #1D5A3E;
}

.status-soon {
    background: #FFF2DF;
    color: #EF8B1D;
}

.status-planned {
    background: #EFE8D7;
    color: #7B776E;
}

.app-card p {
    color: #4F5F4A;
    font-size: 15.5px;
    line-height: 1.5;
    margin: 0;
}

div[data-testid="stButton"] {
    margin-top: -1px;
}

div[data-testid="stVerticalBlock"] > div:has(.app-card) + div .stButton button {
    width: 100%;
    height: 58px;
    border-radius: 0 0 24px 24px;
    border: 1px solid #D7C8A4;
    border-top: none;
    background-color: #FFF7EA;
    color: #EF8B1D;
    font-size: 16px;
    font-weight: 850;
}

div[data-testid="stVerticalBlock"] > div:has(.app-card) + div .stButton button:hover {
    background-color: #EF8B1D;
    color: white;
    border-color: #EF8B1D;
}

.disabled-footer {
    background-color: #F4EFE3;
    border: 1px solid #D7C8A4;
    border-top: none;
    border-radius: 0 0 24px 24px;
    height: 58px;
    color: #7B776E;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 850;
}

.footer-note {
    text-align: center;
    color: #7B776E;
    font-size: 13px;
    margin-top: 34px;
}
</style>
""",
    unsafe_allow_html=True,
)



st.markdown(
    f"""
<div class="app-banner">
    <div class="banner-logo">
        <img src="data:image/png;base64,{logo}" width="100">
    </div>
    <div class="banner-title">
        <h1>Tabby & Jack's Analytics Hub</h1>
        <p>Provides ordering tools, supports daily operations, and assists with other functions of our team.</p>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="section-kicker">Daily Tools</div>
<div class="section-title">Reporting Dashboard</div>
<div class="section-subtitle">Choose a tool below to get started!</div>
""",
    unsafe_allow_html=True,
)


def status_class(status):
    if status == "Available":
        return "status-available"
    if status == "Coming Soon":
        return "status-soon"
    return "status-planned"


def render_icon(tool):
    return f'<img src="data:image/png;base64,{tool["icon"]}" width="50">'


def render_tool_card(tool, key):
    st.markdown(
        f"""
<div class="app-card">
    <div class="app-card-body">
        <div class="app-card-top">
            <div class="app-icon-wrap">
                {render_icon(tool)}
            </div>
            <div>
                <h3>{tool["title"]}</h3>
                <div class="status-pill {status_class(tool["status"])}">{tool["status"]}</div>
            </div>
        </div>
        <p>{tool["description"]}</p>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    if tool["enabled"]:
        if st.button(f"Open {tool['title']}  →", use_container_width=True, key=key):
            st.switch_page(tool["page"])
    else:
        st.markdown(
            f"""
<div class="disabled-footer">{tool["status"]}  →</div>
""",
            unsafe_allow_html=True,
        )


categories = ["Ordering Tools", "Inventory Tools", "Office Hour Tools"]

for category in categories:
    category_tools = [tool for tool in tools if tool["category"] == category]

    st.markdown(
        f"""
<div class="category-title">{category}</div>
""",
        unsafe_allow_html=True,
    )

    for i in range(0, len(category_tools), 2):
        cols = st.columns(2, gap="large")

        for col, tool in zip(cols, category_tools[i:i + 2]):
            with col:
                render_tool_card(
                    tool,
                    key=f"open_{tool['title'].lower().replace(' ', '_')}",
                )


st.markdown(
    """
<div class="footer-note">
    Tabby & Jack's Analytics Hub · Version 1.0 · Built by Maria Swenson for internal use
</div>
""",
    unsafe_allow_html=True,
)
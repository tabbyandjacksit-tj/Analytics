import streamlit as st

st.set_page_config(
    page_title="Tabby & Jack's Analytics",
    page_icon="images/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

pages = {
    "Home": st.Page(
        "pages/home.py",
        title="Home",
        icon=":material/home:",
        default=True
    ),
    "Major Vendor Order": st.Page(
        "pages/MVO.py",
        title="Major Vendor Order",
        icon=":material/shopping_cart:"
    ),
    "Small Vendor Order": st.Page(
        "pages/SVO.py",
        title="Small Vendor Order",
        icon=":material/shopping_basket:"
    ),
    "Dusty Report Transfer": st.Page(
        "pages/dusty.py",
        title="Dusty Report Transfer",
        icon=":material/move_item:"
    ),
    "Sales by Brand": st.Page(
        "pages/brandsale.py",
        title="Sales by Brand",
        icon=":material/filter_list:"
    ),
    "Helpful Links": st.Page(
        "pages/links.py",
        title="Helpful Links",
        icon=":material/link:"
    ),
    "Instacart Upload": st.Page(
    "pages/instacart.py",
    title="Instacart Upload",
    icon=":material/upload_file:"
    ),
    "Vendor Contact": st.Page(
    "pages/vendorcontact.py",
    title="Vendor Contact",
    icon=":material/contact_page:"
    ),
}

report_links = {
    "Major Vendor Order": "pages/MVO.py",
    "Small Vendor Order": "pages/SVO.py",
    "Dusty Report Transfer": "pages/dusty.py",
    "Sales by Brand": "pages/brandsale.py",
    "Helpful Links": "pages/links.py",
    "Instacart Upload": "pages/instacart.py",
    "Vendor Contact": "pages/vendorcontact.py"
}

st.markdown(
    """
<style>
section[data-testid="stSidebar"] {
    background: #5C8067;
    border-right: none;
}

section[data-testid="stSidebar"] * {
    color: #FFF9EF !important;
}

section[data-testid="stSidebar"] input {
    background: #FFF9EF !important;
    color: #1D5A3E !important;
    border: 1px solid #F3A653 !important;
    border-radius: 10px !important;
}

section[data-testid="stSidebar"] input::placeholder {
    color: #777777 !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(255, 249, 239, .25);
}

section[data-testid="stSidebar"] div[data-testid="stButton"] button {
    background-color: #C98335 !important;
    color: #FFF9EF !important;
    border: 1px solid #C98335 !important;
    border-radius: 12px !important;
    height: 42px !important;
    font-weight: 800 !important;
}

section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
    background-color: #F3A653 !important;
    color: #1D5A3E !important;
    border-color: #F3A653 !important;
}

.sidebar-card {
    background: rgba(255,249,239,.10);
    border: 1px solid rgba(255,249,239,.22);
    border-radius: 18px;
    padding: 18px;
    text-align: center;
    margin-bottom: 1.0rem;
}

.sidebar-title {
    font-size: 1.75rem;
    font-weight: 900;
    margin-top: .2rem;
}

.sidebar-subtitle {
    font-size: .85rem;
    opacity: .85;
}

.sidebar-footer {
    position: fixed;
    bottom: 24px;
    font-size: .75rem;
    opacity: .7;
}

header[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stDecoration"] {
    display: none;
}

button[data-testid="stBaseButton-headerNoPadding"] {
    display: none !important;
}

#MainMenu,
footer {
    visibility: hidden;
}
</style>
""",
    unsafe_allow_html=True
)


def sidebar_nav_button(label, page_path):
    if st.button(label, use_container_width=True, key=f"nav_{page_path}"):
        st.switch_page(page_path)


with st.sidebar:

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.image("images/logo.png", width=200)

    st.markdown(
    """
    <div style="text-align: center;">
        <div class="sidebar-title">Tabby & Jack's</div>
        <div class="sidebar-subtitle">Analytics Hub</div>
    </div>
    """,
    unsafe_allow_html=True
    )



    st.markdown("### :material/search: Find a Report")

    search = st.text_input(
        "Search",
        placeholder="Search reports...",
        label_visibility="collapsed"
    )

    if search:
        st.markdown("**Results**")

        matches = {
            name: page
            for name, page in report_links.items()
            if search.lower() in name.lower()
        }

        if matches:
            for name, page in matches.items():
                sidebar_nav_button(f"Open {name}", page)
        else:
            st.caption("Sorry! That report does not exist!")

    st.divider()

    st.markdown("### Navigation")

    sidebar_nav_button(":material/home: Home", "pages/home.py")
    sidebar_nav_button(":material/shopping_cart: Major Vendor Order", "pages/MVO.py")
    sidebar_nav_button(":material/shopping_basket: Small Vendor Order", "pages/SVO.py")
    sidebar_nav_button(":material/move_item: Dusty Report Transfer", "pages/dusty.py")
    sidebar_nav_button(":material/filter_list: Sales by Brand", "pages/brandsale.py")
    sidebar_nav_button(":material/link: Helpful Links", "pages/links.py")
    sidebar_nav_button(":material/upload_file: Instacart Upload", "pages/instacart.py")
    sidebar_nav_button(":material/contact_page: Vendor Contact", "pages/vendorcontact.py")



pg = st.navigation(
    list(pages.values()),
    position="hidden"
)

pg.run()
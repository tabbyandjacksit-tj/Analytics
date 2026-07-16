import streamlit as st


def render_dashboard_hero(
    title: str,
    subtitle: str,
) -> None:
    st.markdown(
        f"""
        <div class="dashboard-hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def apply_dashboard_styles() -> None:
    st.markdown(
        """
        <style>
        .dashboard-hero {
            background-color: #315F43;
            border-radius: 24px;
            padding: 38px 30px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 8px 22px rgba(29, 90, 62, 0.18);
        }

        .dashboard-hero h1 {
            color: #FFF9EF;
            margin: 0;
            font-size: 42px;
            font-weight: 900;
        }

        .dashboard-hero p {
            color: rgba(255, 249, 239, 0.88);
            margin: 10px 0 0 0;
            font-size: 17px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
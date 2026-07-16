import streamlit as st

from utils.tools.images import image_to_base64


def apply_dashboard_styles() -> None:
    """Apply shared styling for category dashboard pages."""

    st.markdown(
        """
        <style>
        .category-banner {
            display: flex;
            align-items: center;
            gap: 26px;
            background: #234B34;
            border-radius: 22px;
            padding: 24px 30px;
            margin-bottom: 28px;
            box-shadow: 0 10px 24px rgba(35, 75, 52, 0.18);
        }

        .category-banner-logo-wrap {
            display: flex;
            align-items: center;
            justify-content: center;
            flex: 0 0 126px;
            width: 126px;
            height: 126px;
            border-radius: 20px;
            background: rgba(255, 249, 239, 0.08);
            border: 1px solid rgba(255, 249, 239, 0.22);
        }

        .category-banner-logo {
            width: 94px;
            height: 94px;
            object-fit: contain;
            border-radius: 4px;
        }

        .category-banner-copy {
            flex: 1;
            min-width: 0;
        }

        .category-banner-title {
            color: #FFF9EF;
            font-size: 2.35rem;
            font-weight: 900;
            line-height: 1.15;
            margin: 0;
        }

        .category-banner-description {
            color: rgba(255, 249, 239, 0.90);
            font-size: 1rem;
            line-height: 1.55;
            margin-top: 18px;
        }

        .dashboard-eyebrow {
            color: #EF8B1D;
            font-size: 0.76rem;
            font-weight: 900;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin: 0 0 12px;
        }

        .dashboard-heading {
            color: #1D5A3E;
            font-size: 2rem;
            font-weight: 900;
            line-height: 1.2;
            margin: 0;
        }

        .dashboard-intro {
            color: #5C7A58;
            font-size: 1rem;
            margin: 8px 0 28px;
        }

        @media (max-width: 750px) {
            .category-banner {
                align-items: flex-start;
                padding: 22px;
            }

            .category-banner-logo-wrap {
                flex-basis: 90px;
                width: 90px;
                height: 90px;
            }

            .category-banner-logo {
                width: 68px;
                height: 68px;
            }

            .category-banner-title {
                font-size: 1.75rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard_banner(
    title: str,
    description: str,
) -> None:
    """Render the green category banner."""

    logo = image_to_base64("images/logo.png")

    banner_html = (
        '<div class="category-banner">'
        '<div class="category-banner-logo-wrap">'
        f'<img class="category-banner-logo" '
        f'src="data:image/png;base64,{logo}" alt="Tabby and Jacks logo">'
        "</div>"
        '<div class="category-banner-copy">'
        f'<div class="category-banner-title">{title}</div>'
        f'<div class="category-banner-description">{description}</div>'
        "</div>"
        "</div>"
    )

    st.markdown(
        banner_html,
        unsafe_allow_html=True,
    )


def render_dashboard_intro(
    eyebrow: str,
    title: str,
    description: str,
) -> None:
    """Render the heading above the dashboard cards."""

    intro_html = (
        '<div class="dashboard-eyebrow">'
        f"{eyebrow}"
        "</div>"
        '<div class="dashboard-heading">'
        f"{title}"
        "</div>"
        '<div class="dashboard-intro">'
        f"{description}"
        "</div>"
    )

    st.markdown(
        intro_html,
        unsafe_allow_html=True,
    )
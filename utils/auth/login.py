from __future__ import annotations

import streamlit as st
import streamlit_authenticator as stauth

from utils.auth.users import (
    get_user_by_email,
    load_authenticator_credentials,
)
from utils.tools.secrets import get_secret


# ==========================================
# Authenticator
# ==========================================

def create_authenticator() -> stauth.Authenticate:
    """Create the authentication manager from active Google Sheet users."""
    credentials = load_authenticator_credentials()

    if not credentials.get("usernames"):
        raise RuntimeError("No active authentication users were found.")

    return stauth.Authenticate(
        credentials=credentials,
        cookie_name="tabby_jacks_analytics_login",
        cookie_key=get_secret("AUTH_COOKIE_KEY"),
        cookie_expiry_days=7,
        auto_hash=False,
    )


# ==========================================
# Login Page Styling
# ==========================================

def apply_login_styles() -> None:
    """Apply Tabby & Jack's branding to the login page."""
    st.markdown(
        """
        <style>
        header[data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stDecoration"] {
            display: none;
        }

        #MainMenu,
        footer {
            visibility: hidden;
        }

        .stApp {
            background:
                radial-gradient(
                    circle at top left,
                    rgba(239, 139, 29, 0.12),
                    transparent 35%
                ),
                linear-gradient(
                    180deg,
                    #F6F1E5 0%,
                    #FFF9EF 100%
                );
        }

        .block-container {
            max-width: 540px;
            padding-top: 3rem;
            padding-bottom: 4rem;
        }

        .login-heading {
            text-align: center;
            margin-bottom: 1.4rem;
        }

        .login-heading h1 {
            color: #1D5A3E;
            font-size: 2.25rem;
            font-weight: 900;
            margin: 0.4rem 0 0;
        }

        .login-heading p {
            color: #5C7A58;
            font-size: 1rem;
            margin-top: 0.35rem;
        }

        div[data-testid="stForm"] {
            background: #FFF9EF;
            border: 1px solid #D7C8A4;
            border-radius: 24px;
            padding: 1.9rem 2rem 2rem;
            box-shadow: 0 16px 42px rgba(29, 90, 62, 0.14);
        }

        div[data-testid="stForm"] h2,
        div[data-testid="stForm"] h3 {
            color: #1D5A3E !important;
            text-align: center;
            font-weight: 900 !important;
        }

        div[data-testid="stTextInput"] label {
            color: #2F372D !important;
            font-weight: 700 !important;
        }

        div[data-testid="stTextInput"] input {
            min-height: 46px;
            background: #FFFFFF !important;
            color: #2F372D !important;
            border: 1px solid #D7C8A4 !important;
            border-radius: 12px !important;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: #1D5A3E !important;
            box-shadow: 0 0 0 1px #1D5A3E !important;
        }

        div[data-testid="stFormSubmitButton"] button {
            width: 100%;
            min-height: 46px;
            border: none !important;
            border-radius: 12px !important;
            background: #1D5A3E !important;
            color: #FFF9EF !important;
            font-size: 1rem;
            font-weight: 800 !important;
        }

        div[data-testid="stFormSubmitButton"] button:hover {
            background: #EF8B1D !important;
            color: #1D5A3E !important;
        }

        div[data-testid="stButton"] button {
            border-radius: 12px !important;
            min-height: 42px;
            font-weight: 700 !important;
        }

        .login-note {
            margin-top: 1rem;
            padding: 1rem 1.1rem;
            background: rgba(29, 90, 62, 0.07);
            border: 1px solid rgba(29, 90, 62, 0.14);
            border-radius: 14px;
            text-align: center;
            color: #5C7A58;
            font-size: 0.9rem;
        }

        .login-note strong {
            color: #1D5A3E;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hide_sidebar_for_login() -> None:
    """Hide the sidebar until the employee successfully logs in."""
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }

        button[data-testid="stSidebarCollapseButton"],
        button[data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==========================================
# Password Help
# ==========================================

@st.dialog("Password Help")
def show_password_help() -> None:
    """Show instructions for employees who forgot their password."""
    st.markdown(
        """
        ### Forgot your password?

        Contact **Maria Swenson** or email
        **tabbyandjacksit@gmail.com** to receive a temporary password.

        After signing in, open **Account Settings** to create a new password.

        Do not use your email-account password for the Analytics Hub.
        """
    )


def render_login_help() -> None:
    """Render password help beneath the login form."""
    st.markdown(
        """
        <div class="login-note">
            <strong>Need help signing in?</strong><br>
            Use your approved Tabby &amp; Jack's email address and
            Analytics Hub password.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "Forgot Password?",
        use_container_width=True,
        key="forgot_password_help",
    ):
        show_password_help()


# ==========================================
# Login Gate
# ==========================================
def render_login_gate() -> stauth.Authenticate:
    """
    Render the login screen and stop execution until authentication succeeds.

    Returns the authenticator after the employee signs in.
    """
    authenticator = create_authenticator()

    authentication_status = st.session_state.get("authentication_status")

    # ==========================================
    # Show Login Page Branding
    # ==========================================

    if authentication_status is not True:
        apply_login_styles()
        hide_sidebar_for_login()

        left, center, right = st.columns([1, 1.15, 1])

        with center:
            st.image(
                "images/logo.png",
                width=180,
            )

        st.markdown(
            """
            <div class="login-heading">
                <h1>Tabby &amp; Jack's</h1>
                <p>Employee Analytics Hub</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ==========================================
    # Login Form
    # ==========================================

    authenticator.login(
        location="main",
        max_login_attempts=5,
        fields={
            "Form name": "Employee Login",
            "Username": "Tabby & Jack's Email",
            "Password": "Password",
            "Login": "Log In",
        },
    )

    authentication_status = st.session_state.get("authentication_status")

    # ==========================================
    # Incorrect Login
    # ==========================================

    if authentication_status is False:
        st.error("The email or password you entered is incorrect.")

        render_login_help()
        st.stop()

    # ==========================================
    # Waiting for Login
    # ==========================================

    if authentication_status is None:
        render_login_help()
        st.stop()

    # ==========================================
    # Logged-In User Validation
    # ==========================================

    username = str(
        st.session_state.get("username", "")
    ).strip().lower()

    user = get_user_by_email(username)

    if user is None or not user.active:
        st.error(
            "This employee account is marked as inactive. "
            "If you believe this is a mistake, contact Maria Swenson "
            "or tabbyandjacksit@gmail.com."
        )

        authenticator.logout(
            button_name="Return to Login",
            location="main",
            key="inactive_account_logout",
        )

        st.stop()

    st.session_state["user_role"] = user.role
    st.session_state["user_email"] = user.email
    st.session_state["user_name"] = user.name

    return authenticator


# ==========================================
# Logout
# ==========================================

def render_logout(
    authenticator: stauth.Authenticate,
) -> None:
    """Show the signed-in employee and logout button in the sidebar."""
    display_name = (
        st.session_state.get("user_name")
        or st.session_state.get("username")
    )

    with st.sidebar:
        st.caption(f"Signed in as {display_name}")

        authenticator.logout(
            button_name="Log Out",
            location="sidebar",
            key="analytics_logout",
            use_container_width=True,
        )
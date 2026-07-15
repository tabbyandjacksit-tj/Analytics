from __future__ import annotations

import streamlit as st
import streamlit_authenticator as stauth

from utils.auth.users import (
    get_user_by_email,
    load_authenticator_credentials,
)
from utils.secrets import get_secret


def create_authenticator() -> stauth.Authenticate:
    """Create the authentication manager from active sheet users."""
    credentials = load_authenticator_credentials()

    if not credentials["usernames"]:
        raise RuntimeError(
            "No active authentication users were found."
        )

    return stauth.Authenticate(
        credentials=credentials,
        cookie_name="tabby_jacks_analytics_login",
        cookie_key=get_secret("AUTH_COOKIE_KEY"),
        cookie_expiry_days=7,
        auto_hash=False,
    )


def render_login_gate() -> stauth.Authenticate:
    """
    Render login and stop execution until the employee is authenticated.

    Returns the authenticator after successful login.
    """
    authenticator = create_authenticator()

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

    authentication_status = st.session_state.get(
        "authentication_status"
    )

    if authentication_status is False:
        st.error(
            "The email or password you entered is incorrect."
        )
        st.stop()

    if authentication_status is None:
        st.info(
            "Enter your approved Tabby & Jack's email "
            "and Analytics Hub password."
        )
        st.stop()

    username = str(
        st.session_state.get("username", "")
    ).strip().lower()

    user = get_user_by_email(username)

    # This rechecks the employee's current status from the cached sheet.
    if user is None or not user.active:
        st.error(
            "This employee account is no longer active."
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


def render_logout(authenticator: stauth.Authenticate) -> None:
    """Show signed-in employee information and a logout button."""
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
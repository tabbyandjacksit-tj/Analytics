from __future__ import annotations

import streamlit as st

from utils.auth import (
    get_user_by_email,
    update_user_password,
    validate_new_password,
    verify_password,
)


st.set_page_config(
    page_title="Account Settings",
    page_icon="images/logo.png",
    layout="wide",
)


st.title("Account Settings")
st.write(
    "Change the password used to access "
    "Tabby & Jack's Analytics."
)


email = str(
    st.session_state.get("user_email", "")
).strip().lower()

if not email:
    st.error("Your signed-in account could not be identified.")
    st.stop()


user = get_user_by_email(email)

if user is None:
    st.error("Your employee account could not be found.")
    st.stop()


with st.form(
    "change_password_form",
    clear_on_submit=True,
):
    current_password = st.text_input(
        "Current password",
        type="password",
        autocomplete="current-password",
    )

    new_password = st.text_input(
        "New password",
        type="password",
        autocomplete="new-password",
    )

    confirm_password = st.text_input(
        "Confirm new password",
        type="password",
        autocomplete="new-password",
    )

    submitted = st.form_submit_button(
        "Change Password",
        use_container_width=True,
    )


if submitted:
    if not verify_password(
        current_password,
        user.password_hash,
    ):
        st.error("Your current password is incorrect.")
        st.stop()

    if new_password != confirm_password:
        st.error("The new passwords do not match.")
        st.stop()

    valid, message = validate_new_password(
        new_password
    )

    if not valid:
        st.error(message)
        st.stop()

    if verify_password(
        new_password,
        user.password_hash,
    ):
        st.error(
            "Your new password must be different "
            "from your current password."
        )
        st.stop()

    try:
        update_user_password(
            email=email,
            new_password=new_password,
        )
    except Exception as exc:
        st.error(
            "Your password could not be updated."
        )
        st.exception(exc)
        st.stop()

    st.success(
        "Your password has been updated successfully."
    )

    st.info(
        "Use your new password the next time you log in."
    )
from __future__ import annotations

import re

import streamlit_authenticator as stauth

from utils.auth.client import get_auth_worksheet
from utils.auth.users import (
    clear_user_cache,
    get_user_by_email,
)


PASSWORD_HASH_HEADER = "Password Hash"


def validate_new_password(password: str) -> tuple[bool, str]:
    """Validate a proposed Analytics Hub password."""
    if len(password) < 12:
        return False, "Password must contain at least 12 characters."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain an uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain a lowercase letter."

    if not re.search(r"\d", password):
        return False, "Password must contain a number."

    if not re.search(r"[^A-Za-z0-9]", password):
        return False, "Password must contain a symbol."

    return True, ""


def verify_password(
    plain_password: str,
    stored_hash: str,
) -> bool:
    """Check whether a plain password matches a stored hash."""
    if not plain_password or not stored_hash:
        return False

    return stauth.Hasher.check_pw(
        plain_password,
        stored_hash,
    )


def hash_password(password: str) -> str:
    """Create a secure hash for a password."""
    return stauth.Hasher.hash(password)


def update_user_password(
    email: str,
    new_password: str,
) -> None:
    """Hash a password and write it into the user's Google Sheet row."""
    user = get_user_by_email(email)

    if user is None:
        raise ValueError("The signed-in employee was not found.")

    if not user.active:
        raise PermissionError("This employee account is inactive.")

    worksheet = get_auth_worksheet()
    headers = worksheet.row_values(1)

    try:
        password_column = headers.index(
            PASSWORD_HASH_HEADER
        ) + 1
    except ValueError as exc:
        raise RuntimeError(
            "The authentication sheet does not contain "
            "a Password Hash column."
        ) from exc

    new_hash = hash_password(new_password)

    worksheet.update_cell(
        user.sheet_row,
        password_column,
        new_hash,
    )

    clear_user_cache()

def set_temporary_password(
    email: str,
    temporary_password: str,
) -> None:
    """Set a temporary password for an employee."""
    valid, message = validate_new_password(
        temporary_password
    )

    if not valid:
        raise ValueError(message)

    update_user_password(
        email=email,
        new_password=temporary_password,
    )
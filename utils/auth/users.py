from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import streamlit as st

from utils.auth.client import get_auth_worksheet
from datetime import datetime
from zoneinfo import ZoneInfo

@dataclass(frozen=True)
class AuthUser:
    email: str
    name: str
    password_hash: str
    role: str
    active: bool
    sheet_row: int


def normalize_active(value: Any) -> bool:
    """Convert spreadsheet values such as TRUE, Yes, or 1 to a boolean."""
    return str(value).strip().lower() in {
        "true",
        "yes",
        "1",
        "active",
    }


@st.cache_data(ttl=60)
def load_users() -> list[AuthUser]:
    """Load all users from the authentication Google Sheet."""
    worksheet = get_auth_worksheet()
    values = worksheet.get_all_values()

    if not values:
        return []

    headers = [str(header).strip() for header in values[0]]

    required_headers = {
        "Email",
        "Name",
        "Password Hash",
        "Role",
        "Active",
    }

    missing_headers = required_headers.difference(headers)

    if missing_headers:
        missing = ", ".join(sorted(missing_headers))
        raise RuntimeError(
            f"Authentication sheet is missing columns: {missing}"
        )

    header_positions = {
        header: index
        for index, header in enumerate(headers)
    }

    users: list[AuthUser] = []

    # Spreadsheet row 1 contains headers, so data begins on row 2.
    for sheet_row, row in enumerate(values[1:], start=2):
        padded_row = row + [""] * (len(headers) - len(row))

        email = padded_row[
            header_positions["Email"]
        ].strip().lower()

        name = padded_row[
            header_positions["Name"]
        ].strip()

        password_hash = padded_row[
            header_positions["Password Hash"]
        ].strip()

        role = padded_row[
            header_positions["Role"]
        ].strip().lower() or "employee"

        active = normalize_active(
            padded_row[header_positions["Active"]]
        )

        if not email:
            continue

        users.append(
            AuthUser(
                email=email,
                name=name or email,
                password_hash=password_hash,
                role=role,
                active=active,
                sheet_row=sheet_row,
            )
        )

    return users


def get_user_by_email(email: str) -> AuthUser | None:
    """Find a user by email address."""
    normalized_email = email.strip().lower()

    for user in load_users():
        if user.email == normalized_email:
            return user

    return None


def load_authenticator_credentials() -> dict:
    """Build the credential structure expected by Streamlit-Authenticator."""
    credentials: dict[str, dict] = {
        "usernames": {}
    }

    for user in load_users():
        if not user.active:
            continue

        if not user.password_hash:
            continue

        if not user.email.endswith("@tabbyandjacks.com"):
            continue

        credentials["usernames"][user.email] = {
            "email": user.email,
            "name": user.name,
            "password": user.password_hash,
            "roles": [user.role],
        }

    return credentials

LOCAL_TIMEZONE = ZoneInfo("America/Chicago")


def _update_user_timestamp(
    email: str,
    column_name: str,
) -> None:
    """Update a timestamp column for a user in the authentication sheet."""
    worksheet = get_auth_worksheet()

    values = worksheet.get_all_values()

    if not values:
        return

    headers = [
        str(header).strip()
        for header in values[0]
    ]

    if column_name not in headers:
        raise RuntimeError(
            f"Authentication sheet is missing column: {column_name}"
        )

    email_column = headers.index("Email") + 1
    target_column = headers.index(column_name) + 1

    normalized_email = email.strip().lower()

    for sheet_row, row in enumerate(values[1:], start=2):
        padded_row = row + [""] * (len(headers) - len(row))

        row_email = padded_row[
            email_column - 1
        ].strip().lower()

        if row_email == normalized_email:
            timestamp = datetime.now(
                LOCAL_TIMEZONE
            ).strftime("%m/%d/%Y %I:%M %p")

            worksheet.update_cell(
                sheet_row,
                target_column,
                timestamp,
            )

            return


def update_last_login(email: str) -> None:
    """Record the user's most recent successful login."""
    _update_user_timestamp(
        email=email,
        column_name="Last Login",
    )


def update_last_edit(email: str) -> None:
    """Record the user's most recent data edit."""
    _update_user_timestamp(
        email=email,
        column_name="Last Edit",
    )


def clear_user_cache() -> None:
    """Force authentication users to be reloaded from Google Sheets."""
    load_users.clear()
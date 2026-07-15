from __future__ import annotations

from typing import Any

import gspread
import streamlit as st
import streamlit_authenticator as stauth
from google.oauth2.service_account import Credentials

from utils.secrets import get_google_service_account, get_secret


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


@st.cache_resource
def get_auth_google_client() -> gspread.Client:
    """Create the Google Sheets client used for authentication."""
    credentials = Credentials.from_service_account_info(
        get_google_service_account(),
        scopes=SCOPES,
    )

    return gspread.authorize(credentials)


def normalize_active(value: Any) -> bool:
    """Convert common spreadsheet values into True or False."""
    return str(value).strip().lower() in {
        "true",
        "yes",
        "1",
        "active",
    }


@st.cache_data(ttl=60)
def load_auth_credentials() -> dict:
    """
    Load active users from the private Analytics Users sheet.

    The one-minute cache avoids requesting the sheet on every Streamlit
    rerun while still allowing staffing changes to take effect quickly.
    """
    client = get_auth_google_client()

    spreadsheet = client.open_by_key(
        get_secret("AUTH_USERS_SHEET_ID")
    )

    worksheet = spreadsheet.worksheet("Users")
    records = worksheet.get_all_records()

    credentials: dict[str, dict] = {
        "usernames": {}
    }

    for row in records:
        email = str(row.get("Email", "")).strip().lower()
        name = str(row.get("Name", "")).strip()
        password_hash = str(
            row.get("Password Hash", "")
        ).strip()
        role = str(row.get("Role", "employee")).strip().lower()
        active = normalize_active(row.get("Active", False))

        if not active:
            continue

        if not email or not password_hash:
            continue

        if not email.endswith("@tabbyandjacks.com"):
            continue

        credentials["usernames"][email] = {
            "email": email,
            "name": name or email,
            "password": password_hash,
            "roles": [role or "employee"],
        }

    return credentials


def create_authenticator() -> stauth.Authenticate:
    """Create the Streamlit authentication manager."""
    credentials = load_auth_credentials()

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
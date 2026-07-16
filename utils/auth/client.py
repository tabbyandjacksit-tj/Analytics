from __future__ import annotations

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

from utils.tools.secrets import get_google_service_account, get_secret


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


@st.cache_resource
def get_auth_google_client() -> gspread.Client:
    """Create and cache the Google Sheets client used for authentication."""
    credentials = Credentials.from_service_account_info(
        get_google_service_account(),
        scopes=SCOPES,
    )

    return gspread.authorize(credentials)


def get_auth_worksheet() -> gspread.Worksheet:
    """Return the Users worksheet from the private authentication sheet."""
    client = get_auth_google_client()

    spreadsheet = client.open_by_key(
        get_secret("AUTH_USERS_SHEET_ID")
    )

    return spreadsheet.worksheet("Users")
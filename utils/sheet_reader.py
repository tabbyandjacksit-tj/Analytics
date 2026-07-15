from typing import Any

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials
from utils.secrets import get_google_service_account



SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


@st.cache_data(ttl=60)
def load_sheet(sheet_id: str, gid: str) -> pd.DataFrame:
    """
    Load a public Google Sheet tab as a DataFrame.

    The result is cached for 60 seconds.
    """
    url = (
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/"
        f"export?format=csv&gid={gid}"
    )

    df = pd.read_csv(url)
    df = df.dropna(how="all")
    df = df.fillna("")

    return df


def get_google_client() -> gspread.Client:
    """Create an authenticated Google Sheets client."""
    credentials = Credentials.from_service_account_info(
        get_google_service_account(),
        scopes=SCOPES,
    )

    return gspread.authorize(credentials)


def get_worksheet(sheet_id: str, worksheet_name: str):
    """Open a worksheet by spreadsheet ID and tab name."""
    client = get_google_client()
    spreadsheet = client.open_by_key(sheet_id)

    return spreadsheet.worksheet(worksheet_name)


def load_private_sheet(
    sheet_id: str,
    worksheet_name: str,
) -> pd.DataFrame:
    """Load an authenticated Google Sheet tab as a DataFrame."""
    worksheet = get_worksheet(sheet_id, worksheet_name)
    values = worksheet.get_all_values()

    if not values:
        return pd.DataFrame()

    headers = [
        str(header).strip().replace("\ufeff", "")
        for header in values[0]
    ]

    rows = values[1:]

    return pd.DataFrame(
        rows,
        columns=headers,
    )


def append_row(
    sheet_id: str,
    worksheet_name: str,
    row_data: dict[str, Any],
    columns: list[str],
) -> None:
    """Append one row to a worksheet."""
    worksheet = get_worksheet(sheet_id, worksheet_name)

    row = [
        row_data.get(column, "")
        for column in columns
    ]

    worksheet.append_row(
        row,
        value_input_option="USER_ENTERED",
    )

    clear_sheet_cache()


def update_row_by_id(
    sheet_id: str,
    worksheet_name: str,
    record_id: str,
    updated_data: dict[str, Any],
    columns: list[str],
    id_column_number: int = 1,
) -> bool:
    """
    Find a row by its ID and replace the row values.

    id_column_number uses Google Sheets numbering, so 1 means column A.
    """
    worksheet = get_worksheet(sheet_id, worksheet_name)
    record_ids = worksheet.col_values(id_column_number)

    try:
        row_number = record_ids.index(record_id) + 1
    except ValueError:
        return False

    last_column_letter = column_number_to_letter(len(columns))

    worksheet.update(
        range_name=f"A{row_number}:{last_column_letter}{row_number}",
        values=[
            [
                updated_data.get(column, "")
                for column in columns
            ]
        ],
    )

    clear_sheet_cache()
    return True


def column_number_to_letter(column_number: int) -> str:
    """Convert a column number to a Google Sheets column letter."""
    letters = ""

    while column_number:
        column_number, remainder = divmod(column_number - 1, 26)
        letters = chr(65 + remainder) + letters

    return letters


def clear_sheet_cache() -> None:
    """Clear cached sheet data after a write operation."""
    load_sheet.clear()
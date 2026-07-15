
def get_google_client() -> gspread.Client:
    """Create an authenticated Google Sheets client."""
    credentials = Credentials.from_service_account_info(
        dict(st.secrets["google_service_account"]),
        scopes=SCOPES,
    )
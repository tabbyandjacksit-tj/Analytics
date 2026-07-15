import json
import os

import streamlit as st


def get_google_service_account():
    """
    Returns the Google service account credentials.

    Uses Streamlit secrets locally and
    Render environment variables when deployed.
    """

    if "google_service_account" in st.secrets:
        return dict(st.secrets["google_service_account"])

    return json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT"])



def get_secret(name: str) -> str:
    if name in st.secrets:
        return str(st.secrets[name])

    value = os.environ.get(name)

    if value is None:
        raise RuntimeError(f"Missing required secret: {name}")

    return value
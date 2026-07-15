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



def get_secret(name):
    if name in st.secrets:
        return st.secrets[name]

    return os.environ[name]
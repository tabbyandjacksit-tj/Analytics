from __future__ import annotations
import json
import os
from typing import Any
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

def _read_local_secrets() -> Any | None:
    """
    Return Streamlit secrets when a local secrets.toml exists.

    Render does not have a secrets.toml file, so accessing st.secrets can
    raise StreamlitSecretNotFoundError. In that case, return None and use
    environment variables instead.
    """
    try:
        # Calling keys() forces Streamlit to parse the secrets file.
        st.secrets.keys()
        return st.secrets
    except StreamlitSecretNotFoundError:
        return None


def get_secret(name: str) -> str:
    """
    Read a required value.

    Locally:
        .streamlit/secrets.toml

    On Render:
        Environment variables
    """
    local_secrets = _read_local_secrets()

    if local_secrets is not None and name in local_secrets:
        return str(local_secrets[name])

    value = os.environ.get(name)

    if value is None or not value.strip():
        raise RuntimeError(
            f"Missing required secret or environment variable: {name}"
        )

    return value


def get_optional_secret(name: str, default: str = "",) -> str:
    """Read an optional value locally or from Render."""
    local_secrets = _read_local_secrets()

    if local_secrets is not None and name in local_secrets:
        return str(local_secrets[name])

    return os.environ.get(name, default)


def get_google_service_account() -> dict[str, Any]:
    """
    Return Google service-account credentials.

    Locally, credentials come from:
        [google_service_account]
        ...

    On Render, credentials come from:
        GOOGLE_SERVICE_ACCOUNT
    """
    local_secrets = _read_local_secrets()

    if (
        local_secrets is not None
        and "google_service_account" in local_secrets
    ):
        return dict(local_secrets["google_service_account"])

    raw_credentials = os.environ.get("GOOGLE_SERVICE_ACCOUNT")

    if not raw_credentials:
        raise RuntimeError(
            "Missing GOOGLE_SERVICE_ACCOUNT environment variable."
        )

    try:
        credentials = json.loads(raw_credentials)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "GOOGLE_SERVICE_ACCOUNT is not valid JSON."
        ) from exc

    if not isinstance(credentials, dict):
        raise RuntimeError(
            "GOOGLE_SERVICE_ACCOUNT must contain a JSON object."
        )

    return credentials
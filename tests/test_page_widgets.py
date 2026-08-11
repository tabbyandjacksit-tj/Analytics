from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_page(relative_path: str) -> AppTest:
    """Load one page with a basic authenticated session."""

    app = AppTest.from_file(
        str(PROJECT_ROOT / relative_path),
        default_timeout=10,
    )

    app.session_state["authentication_status"] = True
    app.session_state["user_name"] = "Test User"
    app.session_state["user_email"] = "test@example.com"
    app.session_state["user_role"] = "Admin"

    app.run(timeout=10)

    exception_messages = [
        str(exception.value)
        for exception in app.exception
    ]

    assert not app.exception, (
        f"{relative_path} raised an exception:\n"
        + "\n".join(exception_messages)
    )

    return app


def button_labels(app: AppTest) -> list[str]:
    """Return the visible button labels."""

    return [
        str(button.label)
        for button in app.button
    ]


def uploader_labels(app: AppTest) -> list[str]:
    """Return the visible file-uploader labels."""

    return [
        str(uploader.label)
        for uploader in app.file_uploader
    ]


def test_home_has_navigation_buttons() -> None:
    app = load_page("pages/home.py")

    labels = button_labels(app)

    assert labels, "The Home page has no navigation buttons."


def test_sales_by_hour_has_upload_box() -> None:
    app = load_page("pages/reports/salesbyhour.py")

    assert len(app.file_uploader) >= 1

    labels = uploader_labels(app)

    assert any(
        "csv" in label.lower()
        or "upload" in label.lower()
        for label in labels
    )


def test_employee_capture_has_upload_box() -> None:
    app = load_page("pages/admin/employeecapture.py")

    assert len(app.file_uploader) >= 1



def test_sales_by_brand_page_has_interactive_input() -> None:
    """
    Sales by Brand should initially show at least one usable input.

    Do not assume a Generate button exists before the required data is entered.
    """

    app = load_page("pages/reports/brandsale.py")

    interactive_count = (
        len(app.file_uploader)
        + len(app.number_input)
        + len(app.date_input)
        + len(app.selectbox)
        + len(app.radio)
        + len(app.button)
    )

    assert interactive_count >= 1


def test_no_visible_button_has_blank_label() -> None:
    """Visible buttons should always have meaningful labels."""

    pages = [
        "pages/home.py",
        "pages/reports/brandsale.py",
        "pages/reports/salesbyhour.py",
        "pages/admin/employeecapture.py",
        "pages/admin/instacart.py",
    ]

    blank_buttons: list[str] = []

    for page_path in pages:
        app = load_page(page_path)

        for button in app.button:
            if not str(button.label).strip():
                blank_buttons.append(page_path)

    assert not blank_buttons, (
        "Blank button labels found on:\n"
        + "\n".join(blank_buttons)
    )
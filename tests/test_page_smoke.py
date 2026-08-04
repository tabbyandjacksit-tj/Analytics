# tests/test_page_smoke.py

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


PAGES = [
    "pages/home.py",
    "pages/dashboards/ordering.py",
    "pages/dashboards/reporting.py",
    "pages/dashboards/employee_resources.py",
    "pages/dashboards/admin_tools.py",
    "pages/reports/MVO.py",
    "pages/reports/SVO.py",
    "pages/reports/brandsale.py",
    "pages/reports/salesbyhour.py",
    "pages/admin/instacart.py",
    "pages/admin/employeecapture.py",
    "pages/admin/sortgrooming.py",
]


@pytest.mark.parametrize("page_path", PAGES)
def test_page_loads_without_exception(page_path: str) -> None:
    page_file = PROJECT_ROOT / page_path

    app = AppTest.from_file(str(page_file))

    # Simulate an already logged-in user if the page expects auth state.
    app.session_state["authentication_status"] = True
    app.session_state["user_name"] = "Test User"
    app.session_state["user_email"] = "test@example.com"
    app.session_state["user_role"] = "Admin"

    app.run(timeout=10)

    assert not app.exception, (
        f"{page_path} raised an exception: "
        f"{[str(error.value) for error in app.exception]}"
    )
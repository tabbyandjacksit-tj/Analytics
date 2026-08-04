from __future__ import annotations

from pathlib import Path

from utils.tools.navigation import (
    PAGE_CONFIG,
    build_breadcrumbs,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Files inside pages/ that are intentionally not registered.
EXCLUDED_PAGE_FILES = {
    "pages/resources/expired.py",
}


def test_all_configured_page_files_exist() -> None:
    """Every path in PAGE_CONFIG must point to a real file."""

    missing: list[str] = []

    for page_id, page in PAGE_CONFIG.items():
        page_path = PROJECT_ROOT / page["path"]

        if not page_path.is_file():
            missing.append(
                f"{page_id}: {page['path']}"
            )

    assert not missing, (
        "Configured page files are missing:\n"
        + "\n".join(sorted(missing))
    )


def test_all_page_files_are_registered() -> None:
    """
    Every active Python page must appear in PAGE_CONFIG.

    Old, archived, or intentionally unused pages can be listed in
    EXCLUDED_PAGE_FILES.
    """

    page_folder = PROJECT_ROOT / "pages"

    actual_pages = {
        path.relative_to(PROJECT_ROOT).as_posix()
        for path in page_folder.rglob("*.py")
        if path.name != "__init__.py"
    }

    actual_pages -= EXCLUDED_PAGE_FILES

    configured_pages = {
        page["path"]
        for page in PAGE_CONFIG.values()
    }

    unregistered = actual_pages - configured_pages
    missing_files = configured_pages - actual_pages

    assert not unregistered, (
        "Page files are not registered:\n"
        + "\n".join(sorted(unregistered))
    )

    assert not missing_files, (
        "Configured page files do not exist:\n"
        + "\n".join(sorted(missing_files))
    )


def test_page_paths_are_unique() -> None:
    """No two page IDs should point to the same file."""

    paths = [
        page["path"]
        for page in PAGE_CONFIG.values()
    ]

    duplicates = {
        path
        for path in paths
        if paths.count(path) > 1
    }

    assert not duplicates, (
        "Duplicate page paths found:\n"
        + "\n".join(sorted(duplicates))
    )


def test_all_parent_page_ids_exist() -> None:
    """Every configured parent must exist in PAGE_CONFIG."""

    invalid: list[str] = []

    for page_id, page in PAGE_CONFIG.items():
        parent_id = page.get("parent")

        if parent_id is not None and parent_id not in PAGE_CONFIG:
            invalid.append(
                f"{page_id} uses missing parent: {parent_id}"
            )

    assert not invalid, "\n".join(invalid)


def test_only_one_default_page_exists() -> None:
    """The application should have exactly one default page."""

    default_pages = [
        page_id
        for page_id, page in PAGE_CONFIG.items()
        if page.get("default", False)
    ]

    assert len(default_pages) == 1, (
        "Exactly one page must have default=True. "
        f"Found: {default_pages}"
    )


def test_default_page_is_home() -> None:
    """Home should remain the default page."""

    assert PAGE_CONFIG["home"].get("default") is True


def test_breadcrumbs_build_without_cycles() -> None:
    """
    Build every breadcrumb.

    build_breadcrumbs should raise if a circular parent relationship exists.
    """

    for page_id in PAGE_CONFIG:
        breadcrumbs = build_breadcrumbs(page_id)

        assert breadcrumbs, (
            f"No breadcrumbs were created for {page_id}."
        )


def test_current_breadcrumb_is_not_clickable() -> None:
    """The last breadcrumb item represents the current page."""

    for page_id in PAGE_CONFIG:
        breadcrumbs = build_breadcrumbs(page_id)

        current_title, current_path = breadcrumbs[-1]

        assert current_title == PAGE_CONFIG[page_id]["title"]
        assert current_path is None
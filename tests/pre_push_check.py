# =======================================================================================
# PRE-PUSH PROJECT CHECK
# =======================================================================================

from __future__ import annotations

import importlib
import py_compile
import sys
from pathlib import Path


# =======================================================================================
# PROJECT SETTINGS
# =======================================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Allow imports such as "utils.styling.base" when this script is
# launched from inside the tests folder.
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
PYTHON_FOLDERS = [
    PROJECT_ROOT / "pages",
    PROJECT_ROOT / "utils",
]

ROOT_PYTHON_FILES = [
    PROJECT_ROOT / "app.py",
]

EXCLUDED_FOLDERS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
}

MODULES_TO_IMPORT = [
    "utils.components.headers",
    "utils.reporting.employee_capture",
    "utils.reporting.instacart",
    "utils.reporting.mvo",
    "utils.reporting.officehours",
    "utils.styling.base",
    "utils.styling.components",
    "utils.styling.dashboard",
    "utils.styling.home",
    "utils.styling.mvo",
    "utils.styling.officehours",
    "utils.styling.vendor",
    "utils.tools.images",
    "utils.tools.secrets",
    "utils.tools.sheet_reader",
    "utils.reporting.salesbyhour",
]


# =======================================================================================
# TERMINAL OUTPUT
# =======================================================================================

def print_success(message: str) -> None:
    print(f"[PASS] {message}")


def print_failure(message: str) -> None:
    print(f"[FAIL] {message}")


def print_section(title: str) -> None:
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


# =======================================================================================
# FILE DISCOVERY
# =======================================================================================

def should_exclude(path: Path) -> bool:
    """Return True when the path belongs to an excluded folder."""
    return any(part in EXCLUDED_FOLDERS for part in path.parts)


def find_python_files() -> list[Path]:
    """Find Python files that should be checked."""
    python_files: list[Path] = []

    for file_path in ROOT_PYTHON_FILES:
        if file_path.exists():
            python_files.append(file_path)

    for folder in PYTHON_FOLDERS:
        if not folder.exists():
            continue

        for file_path in folder.rglob("*.py"):
            if not should_exclude(file_path):
                python_files.append(file_path)

    return sorted(set(python_files))


# =======================================================================================
# SYNTAX CHECK
# =======================================================================================

def check_python_syntax(files: list[Path]) -> list[str]:
    """
    Compile every Python file.

    This catches syntax errors without executing the file.
    """
    failures: list[str] = []

    print_section("1. CHECKING PYTHON SYNTAX")

    if not files:
        failures.append("No Python files were found.")
        print_failure("No Python files were found.")
        return failures

    for file_path in files:
        relative_path = file_path.relative_to(PROJECT_ROOT)

        try:
            py_compile.compile(
                str(file_path),
                doraise=True,
            )
            print_success(str(relative_path))

        except py_compile.PyCompileError as error:
            failures.append(
                f"Syntax error in {relative_path}:\n{error.msg}"
            )
            print_failure(str(relative_path))
            print(error.msg)

        except Exception as error:
            failures.append(
                f"Could not compile {relative_path}: {error}"
            )
            print_failure(f"{relative_path}: {error}")

    return failures


# =======================================================================================
# INTERNAL MODULE IMPORT CHECK
# =======================================================================================

def check_internal_imports() -> list[str]:
    """
    Import shared internal modules.

    Page files are intentionally excluded because importing a Streamlit page
    executes its top-level code and may require secrets, files, or network
    connections.
    """
    failures: list[str] = []

    print_section("2. CHECKING INTERNAL MODULE IMPORTS")

    for module_name in MODULES_TO_IMPORT:
        try:
            importlib.import_module(module_name)
            print_success(module_name)

        except ModuleNotFoundError as error:
            failures.append(
                f"Import failed for {module_name}: {error}"
            )
            print_failure(module_name)
            print(f"       {error}")

        except ImportError as error:
            failures.append(
                f"Import failed for {module_name}: {error}"
            )
            print_failure(module_name)
            print(f"       {error}")

        except Exception as error:
            failures.append(
                f"Module raised an error while importing "
                f"{module_name}: {error}"
            )
            print_failure(module_name)
            print(f"       {type(error).__name__}: {error}")

    return failures


# =======================================================================================
# REQUIRED FILE CHECK
# =======================================================================================

def check_required_files() -> list[str]:
    """Confirm important project files and folders exist."""
    failures: list[str] = []

    print_section("3. CHECKING REQUIRED FILES")

    required_paths = [
        PROJECT_ROOT / "app.py",
        PROJECT_ROOT / "pages",
        PROJECT_ROOT / "utils",
        PROJECT_ROOT / "images",
    ]

    for path in required_paths:
        relative_path = path.relative_to(PROJECT_ROOT)

        if path.exists():
            print_success(str(relative_path))
        else:
            failures.append(f"Missing required path: {relative_path}")
            print_failure(str(relative_path))

    return failures


# =======================================================================================
# MAIN
# =======================================================================================

def main() -> int:
    """Run all pre-push checks and return an exit code."""
    print()
    print("TABBY & JACK'S ANALYTICS HUB")
    print("PRE-PUSH CHECK")
    print(f"Project: {PROJECT_ROOT}")

    python_files = find_python_files()

    failures: list[str] = []
    failures.extend(check_python_syntax(python_files))
    failures.extend(check_internal_imports())
    failures.extend(check_required_files())

    print_section("RESULT")

    if failures:
        print_failure(
            f"{len(failures)} check(s) failed. Do not push yet."
        )

        for number, failure in enumerate(failures, start=1):
            print()
            print(f"{number}. {failure}")

        return 1

    print_success(
        f"All checks passed. Checked {len(python_files)} Python files."
    )
    print("The project is ready for Git commit and push.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
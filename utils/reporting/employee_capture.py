import pandas as pd


REQUIRED_COLUMNS = [
    "ID",
    "Completed",
    "Cancelled",
    "Voided",
    "Total",
    "Date",
    "Register",
    "Shop",
    "Employee",
    "Customer",
    "Source",
]

EXCLUDED_EMPLOYEES = [
    "Ken Lonetree",
    "eCom",
    "Celeste Veenstra",
    "Leah Coyne",
    "Ashley Byer",
    "Michelle Lonergan",
    "Ken Lonergan",
    "Brianna Stearns",
    "David Fidler",
    "Krystal Siedschlag",
    "Nicole LaBelle",
    "Paula White",
]


def find_missing_columns(df: pd.DataFrame) -> list[str]:
    """Return required columns that are missing from the uploaded report."""
    return [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]


def normalize_boolean_column(series: pd.Series) -> pd.Series:
    """Convert common true/false values into Boolean values."""
    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "yes", "1", "checked"])
    )


def prepare_employee_report(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the report and keep only valid completed transactions."""
    cleaned_df = df.copy()

    cleaned_df["Completed"] = normalize_boolean_column(
        cleaned_df["Completed"]
    )
    cleaned_df["Cancelled"] = normalize_boolean_column(
        cleaned_df["Cancelled"]
    )
    cleaned_df["Voided"] = normalize_boolean_column(
        cleaned_df["Voided"]
    )

    cleaned_df["Employee"] = (
        cleaned_df["Employee"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    cleaned_df["Customer"] = (
        cleaned_df["Customer"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    cleaned_df = cleaned_df[
        cleaned_df["Completed"]
        & ~cleaned_df["Cancelled"]
        & ~cleaned_df["Voided"]
    ].copy()

    cleaned_df["Customer Attached"] = (
        cleaned_df["Customer"].ne("")
        & cleaned_df["Customer"].str.lower().ne("nan")
    )

    return cleaned_df


def summarize_employee_capture(
    df: pd.DataFrame,
    employee_name: str,
) -> dict:
    """Calculate customer-capture totals for one employee."""
    employee_df = df[df["Employee"] == employee_name].copy()

    total_sales = len(employee_df)
    attached_sales = int(employee_df["Customer Attached"].sum())
    unattached_sales = total_sales - attached_sales

    capture_rate = (
        attached_sales / total_sales
        if total_sales
        else 0
    )

    return {
        "employee_df": employee_df,
        "total_sales": total_sales,
        "attached_sales": attached_sales,
        "unattached_sales": unattached_sales,
        "capture_rate": capture_rate,
    }


def employee_leaderboard(
    df: pd.DataFrame,
    min_sales: int = 0,
    limit: int | None = None,
) -> pd.DataFrame:
    """Create an employee leaderboard ranked by customer-capture rate."""

    leaderboard = (
        df.groupby("Employee", as_index=False)
        .agg(
            Completed_Sales=("ID", "count"),
            Customers_Attached=("Customer Attached", "sum"),
        )
    )

    leaderboard = leaderboard[
        ~leaderboard["Employee"].isin(EXCLUDED_EMPLOYEES)
    ]

    leaderboard["Missing_Customers"] = (
        leaderboard["Completed_Sales"]
        - leaderboard["Customers_Attached"]
    )

    leaderboard["Capture_Rate"] = (
        leaderboard["Customers_Attached"]
        / leaderboard["Completed_Sales"]
    )

    leaderboard = leaderboard.rename(
        columns={
            "Completed_Sales": "Completed Sales",
            "Customers_Attached": "Customers Attached",
            "Missing_Customers": "Missing Customers",
            "Capture_Rate": "Capture Rate",
        }
    )

    leaderboard = leaderboard[
        leaderboard["Completed Sales"] >= min_sales
    ]

    leaderboard = leaderboard.sort_values(
        by=[
            "Capture Rate",
            "Customers Attached",
            "Completed Sales",
        ],
        ascending=[False, False, False],
    )

    if limit is not None:
        leaderboard = leaderboard.head(limit)

    return leaderboard.reset_index(drop=True)

def get_employee_names(df: pd.DataFrame) -> list[str]:
    return sorted(
        employee
        for employee in df["Employee"].unique()
        if employee and employee not in EXCLUDED_EMPLOYEES
    )
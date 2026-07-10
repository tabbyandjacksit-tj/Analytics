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


def find_missing_columns(df: pd.DataFrame) -> list[str]:
    """Return required columns that are missing from the uploaded report."""
    return [column for column in REQUIRED_COLUMNS if column not in df.columns]


def normalize_boolean_column(series: pd.Series) -> pd.Series:
    """Convert common true/false values into Boolean values."""
    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "yes", "1", "checked"])
    )


def prepare_employee_report(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the transaction report and remove cancelled or voided sales."""
    cleaned_df = df.copy()

    cleaned_df["Cancelled"] = normalize_boolean_column(cleaned_df["Cancelled"])
    cleaned_df["Voided"] = normalize_boolean_column(cleaned_df["Voided"])

    cleaned_df["Employee"] = cleaned_df["Employee"].fillna("").astype(str).str.strip()
    cleaned_df["Customer"] = cleaned_df["Customer"].fillna("").astype(str).str.strip()

    cleaned_df = cleaned_df[
        (~cleaned_df["Cancelled"]) & (~cleaned_df["Voided"])
    ].copy()

    return cleaned_df


def summarize_employee_capture(
    df: pd.DataFrame,
    employee_name: str,
) -> dict:
    """Calculate customer-capture totals for one employee."""
    employee_df = df[df["Employee"] == employee_name].copy()

    employee_df["Customer Attached"] = (
        employee_df["Customer"].ne("")
        & employee_df["Customer"].str.lower().ne("nan")
    )

    total_sales = len(employee_df)
    attached_sales = int(employee_df["Customer Attached"].sum())
    unattached_sales = total_sales - attached_sales

    capture_rate = attached_sales / total_sales if total_sales else 0

    return {
        "employee_df": employee_df,
        "total_sales": total_sales,
        "attached_sales": attached_sales,
        "unattached_sales": unattached_sales,
        "capture_rate": capture_rate,
    }
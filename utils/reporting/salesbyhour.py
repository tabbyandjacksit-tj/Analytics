# =======================================================================================
# IMPORTS
# =======================================================================================

from __future__ import annotations

import pandas as pd


# =======================================================================================
# CONSTANTS
# =======================================================================================

DAY_ORDER = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]

CURRENCY_COLUMNS = {
    "Subtotal",
    "Discounts",
    "Tax",
    "Total Tax",
    "Total",
    "Cost",
    "Profit",
}

SUPPORTED_VALUE_COLUMNS = [
    "Subtotal",
    "Total",
    "Count",
]


# =======================================================================================
# COLUMN VALIDATION
# =======================================================================================

def find_missing_columns(
    dataframe: pd.DataFrame,
    value_column: str,
) -> list[str]:
    """
    Return required columns that are missing from the uploaded report.

    The report must contain:
    - Hour
    - Date
    - The selected value column
    """

    required_columns = {
        "Hour",
        "Date",
        value_column,
    }

    return sorted(
        required_columns - set(dataframe.columns)
    )


# =======================================================================================
# NUMERIC CLEANING
# =======================================================================================

def clean_numeric_column(
    series: pd.Series,
) -> pd.Series:
    """
    Convert currency-formatted or numeric text into numbers.

    Examples:
        "$3,173.78" -> 3173.78
        "44"        -> 44
        "(25.00)"   -> -25.00
    """

    cleaned = (
        series.astype(str)
        .str.strip()
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace("(", "-", regex=False)
        .str.replace(")", "", regex=False)
    )

    return pd.to_numeric(
        cleaned,
        errors="coerce",
    ).fillna(0.0)


# =======================================================================================
# DATE PREPARATION
# =======================================================================================

def create_full_date(
    date_series: pd.Series,
    report_year: int,
) -> pd.Series:
    """
    Add the selected report year to month/day values.

    The Lightspeed report contains dates such as:
        5/1
        5/2
        5/3

    These are converted to full dates such as:
        5/1/2026
    """

    date_text = (
        date_series.astype(str)
        .str.strip()
        .str.replace(
            r"\.0$",
            "",
            regex=True,
        )
    )

    has_year = date_text.str.match(
        r"^\d{1,2}/\d{1,2}/\d{2,4}$"
    )

    completed_dates = date_text.copy()

    completed_dates.loc[~has_year] = (
        completed_dates.loc[~has_year]
        + f"/{int(report_year)}"
    )

    return pd.to_datetime(
        completed_dates,
        errors="coerce",
    )


# =======================================================================================
# REPORT PREPARATION
# =======================================================================================

def prepare_sales_by_hour_data(
    dataframe: pd.DataFrame,
    report_year: int,
    value_column: str = "Subtotal",
) -> pd.DataFrame:
    """
    Clean and prepare the uploaded Sales by Hour report.

    Adds:
    - Full Date
    - Day of Week

    Cleans:
    - Hour
    - Selected value column
    """

    if value_column not in SUPPORTED_VALUE_COLUMNS:
        raise ValueError(
            f"Unsupported value column: {value_column}"
        )

    missing_columns = find_missing_columns(
        dataframe=dataframe,
        value_column=value_column,
    )

    if missing_columns:
        missing_text = ", ".join(missing_columns)

        raise ValueError(
            "The uploaded file is missing the following "
            f"required columns: {missing_text}"
        )

    prepared = dataframe.copy()

    # Clean column names in case the CSV contains extra spaces.
    prepared.columns = (
        prepared.columns.astype(str)
        .str.strip()
    )

    prepared["Hour"] = pd.to_numeric(
        prepared["Hour"],
        errors="coerce",
    )

    prepared[value_column] = clean_numeric_column(
        prepared[value_column]
    )

    prepared["Full Date"] = create_full_date(
        date_series=prepared["Date"],
        report_year=report_year,
    )

    prepared = prepared.dropna(
        subset=[
            "Hour",
            "Full Date",
        ]
    ).copy()

    if prepared.empty:
        raise ValueError(
            "No valid dates or hours could be found in the "
            "uploaded report."
        )

    prepared["Hour"] = (
        prepared["Hour"]
        .round()
        .astype(int)
    )

    prepared["Day of Week"] = (
        prepared["Full Date"]
        .dt.day_name()
    )

    prepared = prepared[
        prepared["Day of Week"].isin(DAY_ORDER)
    ].copy()

    if prepared.empty:
        raise ValueError(
            "No valid weekday information could be created "
            "from the uploaded dates."
        )

    return prepared


# =======================================================================================
# HOURLY TOTALS
# =======================================================================================

def create_hourly_totals_table(
    dataframe: pd.DataFrame,
    value_column: str = "Subtotal",
    start_hour: int | None = None,
    end_hour: int | None = None,
) -> pd.DataFrame:
    """
    Create a weekday-by-hour pivot table containing actual totals.

    Rows:
        Hours

    Columns:
        Sunday through Saturday

    Values:
        Sum of the selected value column
    """

    filtered = filter_hour_range(
        dataframe=dataframe,
        start_hour=start_hour,
        end_hour=end_hour,
    )

    if filtered.empty:
        raise ValueError(
            "No report data exists within the selected hour range."
        )

    totals = filtered.pivot_table(
        index="Hour",
        columns="Day of Week",
        values=value_column,
        aggfunc="sum",
        fill_value=0,
    )

    totals = totals.reindex(
        columns=DAY_ORDER,
        fill_value=0,
    )

    complete_hours = range(
        int(filtered["Hour"].min()),
        int(filtered["Hour"].max()) + 1,
    )

    totals = totals.reindex(
        index=complete_hours,
        fill_value=0,
    )

    totals.index.name = "Sales Hour of Day"
    totals.columns.name = None

    return totals.sort_index(
        ascending=False
    )


# =======================================================================================
# PERCENTAGE HEATMAP
# =======================================================================================

def create_sales_percentage_heatmap(
    dataframe: pd.DataFrame,
    value_column: str = "Subtotal",
    start_hour: int | None = None,
    end_hour: int | None = None,
) -> pd.DataFrame:
    """
    Calculate each weekday-and-hour cell as a percentage of
    the complete selected report total.

    Formula:
        cell total / report total

    Example:
        0.0170 displays as 1.70%
    """

    totals = create_hourly_totals_table(
        dataframe=dataframe,
        value_column=value_column,
        start_hour=start_hour,
        end_hour=end_hour,
    )

    report_total = totals.to_numpy().sum()

    if report_total <= 0:
        raise ValueError(
            "The selected report values do not contain a "
            "positive total."
        )

    percentages = totals / report_total

    percentages.index.name = "Sales Hour of Day"
    percentages.columns.name = None

    return percentages


# =======================================================================================
# HOUR RANGE FILTER
# =======================================================================================

def filter_hour_range(
    dataframe: pd.DataFrame,
    start_hour: int | None = None,
    end_hour: int | None = None,
) -> pd.DataFrame:
    """Filter prepared report data to a selected hour range."""

    filtered = dataframe.copy()

    if start_hour is not None:
        filtered = filtered[
            filtered["Hour"] >= start_hour
        ]

    if end_hour is not None:
        filtered = filtered[
            filtered["Hour"] <= end_hour
        ]

    return filtered.copy()


# =======================================================================================
# TIME LABELS
# =======================================================================================

def format_hour(
    hour: int,
) -> str:
    """
    Convert a 24-hour number into a readable hour.

    Examples:
        0  -> 12 AM
        9  -> 9 AM
        12 -> 12 PM
        15 -> 3 PM
    """

    hour = int(hour) % 24

    if hour == 0:
        return "12 AM"

    if hour < 12:
        return f"{hour} AM"

    if hour == 12:
        return "12 PM"

    return f"{hour - 12} PM"


def format_hour_index(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Replace numeric hour indexes with readable time labels."""

    formatted = dataframe.copy()

    formatted.index = [
        format_hour(hour)
        for hour in formatted.index
    ]

    formatted.index.name = "Sales Hour of Day"

    return formatted


# =======================================================================================
# SUMMARY CALCULATIONS
# =======================================================================================

def get_peak_sales_period(
    percentage_table: pd.DataFrame,
) -> tuple[str, int, float]:
    """
    Return the weekday, hour, and percentage for the largest cell.

    Returns:
        weekday
        hour
        percentage
    """

    if percentage_table.empty:
        raise ValueError(
            "The percentage table is empty."
        )

    stacked = percentage_table.stack()

    if stacked.empty:
        raise ValueError(
            "The percentage table does not contain any values."
        )

    peak_hour, peak_day = stacked.idxmax()
    peak_percentage = float(stacked.max())

    return (
        str(peak_day),
        int(peak_hour),
        peak_percentage,
    )


def get_report_total(
    dataframe: pd.DataFrame,
    value_column: str,
    start_hour: int | None = None,
    end_hour: int | None = None,
) -> float:
    """Return the selected report total for the chosen hour range."""

    filtered = filter_hour_range(
        dataframe=dataframe,
        start_hour=start_hour,
        end_hour=end_hour,
    )

    return float(
        filtered[value_column].sum()
    )
"""
Sales by Hour reporting helpers.
"""

from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt


REQUIRED_COLUMNS = [
    "Date",
    "Hour",
    "Count",
]


# =============================================================================
# Validation
# =============================================================================
def find_missing_columns(df: pd.DataFrame) -> list[str]:
    return [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]


# =============================================================================
# Cleaning
# =============================================================================
def prepare_sales_hour_report(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce",
    )

    df["Count"] = pd.to_numeric(
        df["Count"],
        errors="coerce",
    ).fillna(0)

    df["Day"] = df["Date"].dt.day_name()

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    df["Day"] = pd.Categorical(
        df["Day"],
        categories=day_order,
        ordered=True,
    )

    return df


# =============================================================================
# Heatmap calculations
# =============================================================================
def build_heatmap(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    grouped = (
        df.groupby(
            ["Day", "Hour"],
            observed=False,
        )["Count"]
        .sum()
        .reset_index()
    )

    heatmap = grouped.pivot(
        index="Day",
        columns="Hour",
        values="Count",
    ).fillna(0)

    if mode == "Average Transactions":
        weeks = max(df["Date"].dt.isocalendar().week.nunique(), 1)
        heatmap = heatmap / weeks

    elif mode == "Percent of Sales":
        total = heatmap.values.sum()

        if total > 0:
            heatmap = heatmap / total * 100

    return heatmap


# =============================================================================
# Plot
# =============================================================================
def create_heatmap(
    heatmap: pd.DataFrame,
    mode: str,
):
    fig, ax = plt.subplots(figsize=(14, 5))

    image = ax.imshow(
        heatmap.values,
        aspect="auto",
        cmap="RdPu",      # Pink → Purple
    )

    ax.set_xticks(range(len(heatmap.columns)))
    ax.set_xticklabels(
        heatmap.columns,
        rotation=45,
        ha="right",
    )

    ax.set_yticks(range(len(heatmap.index)))
    ax.set_yticklabels(heatmap.index)

    if mode == "Percent of Sales":
        fmt = "{:.1f}%"

    else:
        fmt = "{:.1f}"

    for row in range(heatmap.shape[0]):
        for col in range(heatmap.shape[1]):
            ax.text(
                col,
                row,
                fmt.format(
                    heatmap.iloc[row, col]
                ),
                ha="center",
                va="center",
                fontsize=8,
            )

    ax.set_xlabel("Hour")
    ax.set_ylabel("Day")

    cbar = fig.colorbar(image)

    if mode == "Percent of Sales":
        cbar.set_label("% of Weekly Sales")

    else:
        cbar.set_label("Average Transactions")

    plt.tight_layout()

    return fig
import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ["Stock", "Sold", "UPC"]

def find_missing_columns(df: pd.DataFrame) -> list[str]:
    """
    Ensures that the required columns are present in the dataframe.

    Returns a list of missing columns from the REQUIRED_COLUMNS list.
    """
    return [col for col in REQUIRED_COLUMNS if col not in df.columns]

def calculate_order_quantities(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the order quantities based on the following rules:
    - If Stock <= 0 and Sold == 1, Order Qty = 2
    - If Stock <= 0, Order Qty = Sold * (3/4)
    - If Stock < 2, Order Qty = Sold / 2
    - If (Sold / 2) - Stock < 0, Order Qty = 0
    - Otherwise, Order Qty = (Sold / 2) - Stock
    These rules are equivalent to the language used in LS analytics, but are expressed in LS R-Series terms 
    """
    df = df.copy()

    df["Order Qty"] = np.where(
        (df["Stock"] <= 0) & (df["Sold"] == 1),
        2,
        np.where(
            df["Stock"] <= 0,
            df["Sold"] * (3 / 4),
            np.where(
                df["Stock"] < 2,
                df["Sold"] / 2,
                np.where(
                    (df["Sold"] / 2) - df["Stock"] < 0,
                    0,
                    (df["Sold"] / 2) - df["Stock"],
                ),
            ),
        ),
    )

    df["Order Qty"] = np.ceil(df["Order Qty"])
    df["Order Qty"] = np.maximum(0, df["Order Qty"])
    df["Order Qty"] = df["Order Qty"].astype(int)

    output_df = df[df["Order Qty"] > 0].copy()
    output_df = output_df.sort_values("Order Qty", ascending=False)

    for column in output_df.select_dtypes(
        include=["float", "float64"],
    ).columns:
        non_null_values = output_df[column].dropna()

        if (
            not non_null_values.empty
            and (non_null_values % 1 == 0).all()
        ):
            output_df[column] = output_df[column].astype(
                "Int64"
            )
    return output_df
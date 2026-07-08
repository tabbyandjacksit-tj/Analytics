import numpy as np
import pandas as pd


REQUIRED_COLUMNS = ["Stock", "Sold", "UPC"]


def find_missing_columns(df: pd.DataFrame) -> list[str]:
    return [col for col in REQUIRED_COLUMNS if col not in df.columns]


def calculate_order_quantities(df: pd.DataFrame) -> pd.DataFrame:
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

    return output_df
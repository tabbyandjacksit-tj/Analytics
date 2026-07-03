import os
import re
import pandas as pd


def extract_size(text):
    text = str(text)

    size_patterns = (
        r"(\d+(?:\.\d+)?\s?(?:oz|ounce|ounces|lb|lbs|pound|pounds|kg|g|gram|grams|count|ct|pk|pack|#))"
        r"|(\b(?:xxxs|xxs|xs|xsm|sm|small|sml|m|med|medium|l|lg|large|lrg|xl|xxl|xxxl|2xs|3xs|2xl|3xl)\b)"
        r"|(\d+(?:\.\d+)?\s?(?:\"|in|inch|inches|-in))"
        r"|(\d+(?:\.\d+)?\s?(?:\'|ft|feet))"
        r"|(\b(?:pint|pt|qt|quart|ml|liter|litre|gal|gallon|cup|single)\b)"
    )

    match = re.search(size_patterns, text, flags=re.IGNORECASE)

    if not match:
        return "1 ct"

    size = match.group(0).strip()

    size = re.sub(r"(?<=\d)(?=[a-zA-Z])", " ", size)

    return size


def create_instacart_files(report_file, sales_file, output_folder):
    store_data = pd.read_csv(
        report_file,
        dtype=str,
        keep_default_na=False
    )

    # Clean column names
    store_data.columns = (
        store_data.columns
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    store_numbers = {
        "Verona -Tabby & Jack's": 9,
        "Sun Prairie - Tabby & Jack's": 5,
        "Stoughton - Tabby & Jack's": 3,
        "Oregon - Tabby & Jack's": 6,
        "Monona Drive - Tabby & Jack's": 4,
        "Middleton - Tabby & Jack's": 2,
        "Fitchburg - Tabby & Jack's": 1,
        "East Washington - Tabby & Jack's": 7,
        "Cross Plains- Tabby & Jack's": 8
    }

    store_columns = {
        "Verona -Tabby & Jack's": "Verona -Tabby & Jack's",
        "Sun Prairie - Tabby & Jack's": "Sun Prairie - Tabby & Jack's",
        "Stoughton - Tabby & Jack's": "Stoughton - Tabby & Jack's",
        "Oregon - Tabby & Jack's": "Oregon - Tabby & Jack's",
        "Monona Drive - Tabby & Jack's": "Monona Drive - Tabby & Jack's",
        "Middleton - Tabby & Jack's": "Middleton - Tabby & Jack's",
        "Fitchburg - Tabby & Jack's": "Fitchburg - Tabby & Jack's",
        "East Washington - Tabby & Jack's": "East Washington - Tabby & Jack's",
        "Cross Plains- Tabby & Jack's": "Cross Plains- Tabby & Jack's"
    }

    # Build text to search for size
    size_search_cols = [
        "Item",
        "Category",
        "Subcategory 1",
        "Subcategory 2",
        "Subcategory 3",
        "Subcategory 4",
        "Subcategory 5",
        "Subcategory 6",
        "Subcategory 7",
        "Subcategory 8",
        "Subcategory 9"
    ]

    existing_size_cols = [c for c in size_search_cols if c in store_data.columns]

    store_data["size_search_text"] = (
        store_data[existing_size_cols]
        .fillna("")
        .agg(" ".join, axis=1)
    )

    store_data["size"] = store_data["size_search_text"].apply(extract_size)

    sales = pd.read_csv(sales_file, dtype=str, keep_default_na=False)

    sales = sales[
        [
            "lookup_code",
            "sale_price_cents",
            "sale_start_at",
            "sale_end_at"
        ]
    ].drop_duplicates(subset="lookup_code")

    created_files = []

    for store, qty_col in store_columns.items():
        if qty_col not in store_data.columns:
            continue

        store_data[qty_col] = pd.to_numeric(
            store_data[qty_col],
            errors="coerce"
        ).fillna(0)

        # This clears out 0s per store
        filtered = store_data[store_data[qty_col] > 0].copy()

        filtered = filtered[
            [
                "UPC",
                "Item",
                "Brand",
                "size",
                "Price",
                qty_col
            ]
        ]

        filtered.rename(columns={
            "UPC": "lookup_code",
            "Item": "item_name",
            "Brand": "brand_name",
            "Price": "price",
            qty_col: "quantity"
        }, inplace=True)

        filtered = filtered.merge(
            sales,
            on="lookup_code",
            how="left"
        )

        filtered["cost_unit"] = "each"
        filtered["alcoholic"] = "FALSE"

        filtered.drop(columns=["quantity"], inplace=True)

        filtered = filtered[
            [
                "lookup_code",
                "item_name",
                "brand_name",
                "size",
                "price",
                "sale_price_cents",
                "sale_start_at",
                "sale_end_at",
                "cost_unit",
                "alcoholic"
            ]
        ]

        safe_name = store.replace(" - ", "_").replace(" ", "_").replace("'", "")
        safe_name = safe_name.replace("-", "_")
        safe_name = f"{store_numbers[store]}_{safe_name}.csv"

        output_path = output_folder / safe_name

        filtered.to_csv(
            output_path,
            index=False,
            quoting=1,
            encoding="utf-8-sig",
            lineterminator="\n"
        )

        created_files.append(output_path)

    return created_files
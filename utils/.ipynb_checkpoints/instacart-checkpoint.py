import os
import re
import pandas as pd
import paramiko
import streamlit as st


def create_instacart_files(report_file, sales_file, output_folder):
    data = pd.read_csv(
        report_file,
        header=[0, 1],
        dtype=str,
        keep_default_na=False
    )

    data.columns = [
        f"{a.strip()}_{b.strip()}" if "Unnamed" not in a else b.strip()
        for a, b in data.columns.to_flat_index()
    ]

    data.rename(columns=lambda x: x.replace(" ", "_"), inplace=True)

    store_data = pd.DataFrame(data)

    attribute_cols = [
        c for c in store_data.columns
        if "Description" in c or "Attribute" in c
    ]

    store_data["attributes"] = store_data[attribute_cols].fillna("").agg(" ".join, axis=1)

    size_patterns = (
        r"(\d+(?:\.\d+)?\s?(?:oz|lb|lbs|kg|g|count|ct|pk|pack|#))"
        r"|(\b(?:xxxs|xxs|xs|sm|small|m|med|medium|l|lg|large|xl|xxl|xxxl|short|long|xsm|sml|lrg|2xs|3xs|3xl|2xl)\b)"
        r"|(\d+(?:\.\d+)?\s?(?:\"|in|inch|inches|-in))"
        r"|(\d+(?:\.\d+)?\s?(?:\'|ft|feet))"
        r"|(\b(?:pint|pt|qt|quart|ml|single|liter|gal|gallon|cup)\b)"
    )

    store_data["size"] = (
        store_data["attributes"]
        .str.extract(size_patterns, flags=re.IGNORECASE)
        .fillna("")
        .agg("".join, axis=1)
        .str.strip()
    )

    store_data["size"] = store_data["size"].str.replace(
        r"(?<=\d)(?=[a-zA-Z])",
        " ",
        regex=True
    )

    store_data["size"] = store_data["size"].replace("", "1 ct")

    store_numbers = {
        "Verona - Tabby & Jack's": 9,
        "Sun Prairie - Tabby & Jack's": 5,
        "Stoughton - Tabby & Jack's": 3,
        "Oregon - Tabby & Jack's": 6,
        "Monona Drive - Tabby & Jack's": 4,
        "Middleton - Tabby & Jack's": 2,
        "Fitchburg - Tabby & Jack's": 1,
        "East Washington - Tabby & Jack's": 7,
        "Cross Plains - Tabby & Jack's": 8
    }

    description_cols = [c for c in attribute_cols if "Description" in c]

    store_data["Description"] = (
        store_data[description_cols]
        .fillna("")
        .agg(" ".join, axis=1)
    )

    store_data.drop(
        columns=[c for c in attribute_cols if "Attribute" in c] + ["attributes"],
        inplace=True
    )

    store_columns = {
        "Verona - Tabby & Jack's": "Verona_-Tabby_&_Jack's_Quantity_on_Hand",
        "Sun Prairie - Tabby & Jack's": "Sun_Prairie_-_Tabby_&_Jack's_Quantity_on_Hand",
        "Stoughton - Tabby & Jack's": "Stoughton_-_Tabby_&_Jack's_Quantity_on_Hand",
        "Oregon - Tabby & Jack's": "Oregon_-_Tabby_&_Jack's_Quantity_on_Hand",
        "Monona Drive - Tabby & Jack's": "Monona_Drive_-_Tabby_&_Jack's_Quantity_on_Hand",
        "Middleton - Tabby & Jack's": "Middleton_-_Tabby_&_Jack's_Quantity_on_Hand",
        "Fitchburg - Tabby & Jack's": "Fitchburg_-_Tabby_&_Jack's_Quantity_on_Hand",
        "East Washington - Tabby & Jack's": "East_Washington_-_Tabby_&_Jack's_Quantity_on_Hand",
        "Cross Plains - Tabby & Jack's": "Cross_Plains-_Tabby_&_Jack's_Quantity_on_Hand"
    }

    price_col = [c for c in store_data.columns if "Price" in c][0]

    sales = pd.read_csv(sales_file, dtype=str)

    sales = sales[
        [
            "lookup_code",
            "sale_price_cents",
            "sale_start_at",
            "sale_end_at"
        ]
    ]

    sales = sales.drop_duplicates(subset="lookup_code")

    created_files = []

    for store, qty_col in store_columns.items():
        if qty_col not in store_data.columns:
            continue

        store_data[qty_col] = pd.to_numeric(
            store_data[qty_col],
            errors="coerce"
        ).fillna(0)

        filtered = store_data[store_data[qty_col] > 0].copy()

        filtered = filtered[
            ["UPC", "Description", "Store_Brand", price_col, "size", qty_col]
        ]

        filtered.rename(columns={
            "UPC": "lookup_code",
            "Description": "item_name",
            "Store_Brand": "brand_name",
            price_col: "price",
            qty_col: "quantity"
        }, inplace=True)

        filtered = filtered.merge(sales, on="lookup_code", how="left")

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


def upload_files_to_instacart(files):
    host = st.secrets["INSTACART_HOST"]
    username = st.secrets["INSTACART_USERNAME"]
    password = st.secrets["INSTACART_PASSWORD"]

    remote_base = "/inventory-files"

    remote_folders = {
        "1": "339872-tabby_jacks-1",
        "2": "339871-tabby_jacks-2",
        "3": "339862-tabby_jacks-3",
        "4": "339865-tabby_jacks-4",
        "5": "339864-tabby_jacks-5",
        "6": "339870-tabby_jacks-6",
        "7": "339863-tabby_jacks-7",
        "8": "339869-tabby_jacks-8",
        "9": "339868-tabby_jacks-9",
    }

    transport = paramiko.Transport((host, 22))
    transport.connect(username=username, password=password)

    sftp = paramiko.SFTPClient.from_transport(transport)

    uploaded = []

    try:
        for file_path in files:
            file_name = os.path.basename(file_path)
            store_number = file_name.split("_")[0]

            remote_folder = remote_folders.get(store_number)

            if not remote_folder:
                continue

            remote_path = f"{remote_base}/{remote_folder}/{file_name}"

            sftp.put(str(file_path), remote_path)

            uploaded.append(file_name)

    finally:
        sftp.close()
        transport.close()

    return uploaded
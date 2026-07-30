# =======================================================================================
# IMPORTS
# =======================================================================================

from datetime import date

import pandas as pd
import streamlit as st

from utils.components.headers import render_section_header
from utils.reporting.salesbyhour import (
    SUPPORTED_VALUE_COLUMNS,
    create_hourly_totals_table,
    create_sales_percentage_heatmap,
    format_hour,
    format_hour_index,
    get_peak_sales_period,
    get_report_total,
    prepare_sales_by_hour_data,
)
from utils.styling.base import (
    apply_base_styles,
    render_hero,
)
from utils.styling.components import apply_component_styles


# =======================================================================================
# PAGE CONFIGURATION
# =======================================================================================

st.set_page_config(
    page_title="Sales by Hour",
    page_icon="images/logo.png",
    layout="wide",
)

apply_base_styles(max_width=1160)
apply_component_styles()


# =======================================================================================
# PAGE HEADER
# =======================================================================================

render_hero(
    "Sales by Hour",
    (
        "Upload a Sales by Hour report to create a heatmap "
        "showing when sales occur throughout the week."
    ),
)


# =======================================================================================
# REPORT UPLOAD
# =======================================================================================

render_section_header(
    label="Report Setup",
    title="Upload Sales by Hour Report",
    subtitle=(
        "Upload the CSV exported from Lightspeed and select "
        "the year represented by the report dates."
    ),
)

settings_column, upload_column = st.columns(
    [1, 2],
    gap="large",
)

with settings_column:
    report_year = st.number_input(
        "Report Year",
        min_value=2020,
        max_value=2100,
        value=date.today().year,
        step=1,
        help=(
            "The exported report only includes month and day, "
            "so the year is needed to determine weekdays."
        ),
    )

    value_column = st.selectbox(
        "Calculate Heatmap Using",
        options=SUPPORTED_VALUE_COLUMNS,
        index=0,
        help=(
            "Subtotal and Total calculate sales distribution. "
            "Count calculates transaction distribution."
        ),
    )

with upload_column:
    uploaded_file = st.file_uploader(
        "Upload Sales by Hour CSV",
        type=["csv"],
        key="sales_by_hour_file",
        help=(
            "Export the Sales by Hour report from Lightspeed "
            "as a CSV file."
        ),
    )

    st.caption(
        "Required columns: Hour, Date, and the selected "
        "calculation column."
    )


# =======================================================================================
# WAIT FOR FILE
# =======================================================================================

if uploaded_file is None:
    st.info(
        "Upload a Sales by Hour CSV file to create the report."
    )
    st.stop()


# =======================================================================================
# READ FILE
# =======================================================================================

try:
    raw_data = pd.read_csv(
        uploaded_file,
    )

except Exception as error:
    st.error(
        "The uploaded CSV could not be read."
    )
    st.exception(error)
    st.stop()


# =======================================================================================
# PREPARE DATA
# =======================================================================================

try:
    prepared_data = prepare_sales_by_hour_data(
        dataframe=raw_data,
        report_year=int(report_year),
        value_column=value_column,
    )

except ValueError as error:
    st.error(str(error))
    st.stop()

except Exception as error:
    st.error(
        "An unexpected error occurred while preparing the report."
    )
    st.exception(error)
    st.stop()


# =======================================================================================
# HOUR RANGE SETTINGS
# =======================================================================================

available_start_hour = int(
    prepared_data["Hour"].min()
)

available_end_hour = int(
    prepared_data["Hour"].max()
)

render_section_header(
    label="Display Settings",
    title="Choose Hours to Include",
    subtitle=(
        "Adjust the hour range to remove times when the stores "
        "are normally closed."
    ),
)

hour_column_1, hour_column_2 = st.columns(
    2,
    gap="large",
)

with hour_column_1:
    start_hour = st.number_input(
        "Starting Hour",
        min_value=0,
        max_value=23,
        value=available_start_hour,
        step=1,
        format="%d",
        help="Hours use the 24-hour clock.",
    )

    st.caption(
        f"Starts at {format_hour(int(start_hour))}"
    )

with hour_column_2:
    end_hour = st.number_input(
        "Ending Hour",
        min_value=0,
        max_value=23,
        value=available_end_hour,
        step=1,
        format="%d",
        help="Hours use the 24-hour clock.",
    )

    st.caption(
        f"Ends at {format_hour(int(end_hour))}"
    )

if start_hour > end_hour:
    st.error(
        "The starting hour must be earlier than or equal to "
        "the ending hour."
    )
    st.stop()


# =======================================================================================
# CREATE REPORT TABLES
# =======================================================================================

try:
    percentage_table = create_sales_percentage_heatmap(
        dataframe=prepared_data,
        value_column=value_column,
        start_hour=int(start_hour),
        end_hour=int(end_hour),
    )

    totals_table = create_hourly_totals_table(
        dataframe=prepared_data,
        value_column=value_column,
        start_hour=int(start_hour),
        end_hour=int(end_hour),
    )

    report_total = get_report_total(
        dataframe=prepared_data,
        value_column=value_column,
        start_hour=int(start_hour),
        end_hour=int(end_hour),
    )

    peak_day, peak_hour, peak_percentage = (
        get_peak_sales_period(
            percentage_table=percentage_table,
        )
    )

except ValueError as error:
    st.error(str(error))
    st.stop()

except Exception as error:
    st.error(
        "The Sales by Hour report could not be created."
    )
    st.exception(error)
    st.stop()


# =======================================================================================
# SUMMARY METRICS
# =======================================================================================

render_section_header(
    label="Report Summary",
    title="Sales Distribution Overview",
    subtitle=(
        "Review the report total and the busiest sales period."
    ),
)

metric_column_1, metric_column_2, metric_column_3 = (
    st.columns(
        3,
        gap="large",
    )
)

with metric_column_1:
    if value_column == "Count":
        st.metric(
            "Total Transactions",
            f"{report_total:,.0f}",
        )
    else:
        st.metric(
            f"Total {value_column}",
            f"${report_total:,.2f}",
        )

with metric_column_2:
    st.metric(
        "Busiest Period",
        f"{peak_day} at {format_hour(peak_hour)}",
    )

with metric_column_3:
    st.metric(
        "Percentage of Report",
        f"{peak_percentage:.2%}",
    )


# =======================================================================================
# HEATMAP
# =======================================================================================

render_section_header(
    label="Heatmap",
    title=f"{value_column} by Day and Hour",
    subtitle=(
        "Each cell shows the percentage of the selected report "
        "total generated during that weekday and hour."
    ),
)

display_percentage_table = format_hour_index(
    percentage_table
)

# Change the cmap value later to adjust the heatmap colors.
#
# Common options:
#   "RdYlGn"
#   "YlGn"
#   "Blues"
#   "Greens"
#   "Oranges"
#
styled_heatmap = (
    display_percentage_table.style
    .format("{:.2%}")
    .background_gradient(
        cmap="RdYlGn",
        axis=None,
    )
    .set_properties(
        **{
            "text-align": "center",
        }
    )
    .set_table_styles(
        [
            {
                "selector": "th",
                "props": [
                    ("text-align", "center"),
                    ("font-weight", "700"),
                ],
            },
            {
                "selector": "td",
                "props": [
                    ("text-align", "center"),
                ],
            },
        ]
    )
)

st.dataframe(
    styled_heatmap,
    width="stretch",
    height=620,
)


# =======================================================================================
# ACTUAL TOTALS
# =======================================================================================

with st.expander(
    f"View Actual {value_column} Totals",
):
    display_totals_table = format_hour_index(
        totals_table
    )

    if value_column == "Count":
        styled_totals = (
            display_totals_table.style
            .format("{:,.0f}")
        )
    else:
        styled_totals = (
            display_totals_table.style
            .format("${:,.2f}")
        )

    st.dataframe(
        styled_totals,
        width="stretch",
    )


# =======================================================================================
# SOURCE DATA
# =======================================================================================

with st.expander(
    "View Prepared Report Data",
):
    source_columns = [
        "Full Date",
        "Day of Week",
        "Hour",
        value_column,
    ]

    source_data = (
        prepared_data[source_columns]
        .sort_values(
            by=[
                "Full Date",
                "Hour",
            ]
        )
        .reset_index(
            drop=True
        )
    )

    st.dataframe(
        source_data,
        width="stretch",
        hide_index=True,
    )
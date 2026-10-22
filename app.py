
from pathlib import Path

import pandas as pd
import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide",
)

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "retail_sales_clean.csv"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path, parse_dates=["Date"])
    return data


# --------------------------------------------------
# DASHBOARD HEADER
# --------------------------------------------------

st.title("📊 Retail Sales Dashboard")
st.write(
    "Explore retail transactions, revenue, products, "
    "and regional performance."
)

st.divider()

if not DATA_FILE.exists():
    st.error(f"Dataset not found: {DATA_FILE}")
    st.stop()

df = load_data(str(DATA_FILE))

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

regions = sorted(df["Region"].dropna().unique().tolist())
products = sorted(df["Product"].dropna().unique().tolist())
payment_methods = sorted(
    df["Payment_Method"].dropna().unique().tolist()
)

selected_regions = st.sidebar.multiselect(
    "Select regions",
    options=regions,
    default=regions,
)

selected_products = st.sidebar.multiselect(
    "Select products",
    options=products,
    default=products,
)

selected_payments = st.sidebar.multiselect(
    "Select payment methods",
    options=payment_methods,
    default=payment_methods,
)

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        filtered_df["Date"].dt.date.between(
            start_date,
            end_date,
        )
    ]

filtered_df = filtered_df[
    filtered_df["Region"].isin(selected_regions)
    & filtered_df["Product"].isin(selected_products)
    & filtered_df["Payment_Method"].isin(selected_payments)
]

# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

st.subheader("Business Overview")

total_revenue = filtered_df["Revenue"].sum()
total_transactions = filtered_df["Transaction_ID"].nunique()
total_units = filtered_df["Quantity"].sum()

average_transaction = (
    total_revenue / total_transactions
    if total_transactions > 0
    else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"{total_revenue:,.2f}",
)

col2.metric(
    "Transactions",
    f"{total_transactions:,}",
)

col3.metric(
    "Units Sold",
    f"{total_units:,.0f}",
)

col4.metric(
    "Average Transaction Value",
    f"{average_transaction:,.2f}",
)

st.caption(
    f"Showing {len(filtered_df):,} of {len(df):,} records. "
    "Revenue currency has not yet been confirmed."
)

st.divider()

# --------------------------------------------------
# SALES BY PRODUCT
# --------------------------------------------------

st.subheader("Product Performance")

if filtered_df.empty:
    st.warning("No transactions match the selected filters.")
else:
    product_sales = (
        filtered_df.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(product_sales)

# --------------------------------------------------
# SALES BY REGION
# --------------------------------------------------

st.subheader("Regional Performance")

if not filtered_df.empty:
    region_sales = (
        filtered_df.groupby("Region")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(region_sales)

# --------------------------------------------------
# MONTHLY SALES TREND
# --------------------------------------------------

st.subheader("Monthly Revenue Trend")

if not filtered_df.empty:
    monthly_sales = (
        filtered_df.assign(
            Month=filtered_df["Date"].dt.to_period("M").dt.to_timestamp()
        )
        .groupby("Month")["Revenue"]
        .sum()
        .sort_index()
    )

    st.line_chart(monthly_sales)

# --------------------------------------------------
# TRANSACTION TABLE
# --------------------------------------------------

st.subheader("Filtered Transactions")

st.dataframe(
    filtered_df[
        [
            "Transaction_ID",
            "Date",
            "Customer_ID",
            "Product",
            "Region",
            "Payment_Method",
            "Quantity",
            "Unit_Price",
            "Revenue",
        ]
    ].sort_values("Date", ascending=False),
    use_container_width=True,
    hide_index=True,
)

# --------------------------------------------------
# DOWNLOAD FILTERED DATA
# --------------------------------------------------

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Transactions (CSV)",
    data=csv_data,
    file_name="filtered_retail_sales.csv",
    mime="text/csv",
)

st.caption("Retail Sales Dashboard | Built with Python, Pandas and Streamlit")

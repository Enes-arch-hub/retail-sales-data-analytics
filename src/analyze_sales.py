
from pathlib import Path
import pandas as pd

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "processed" / "retail_sales_clean.csv"
REPORT_DIR = PROJECT_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

# Load cleaned data
df = pd.read_csv(DATA_FILE, parse_dates=["Date"])

print("=" * 65)
print("RETAIL SALES ANALYSIS")
print("=" * 65)

# 1. Overall business summary
print("\n1. OVERALL BUSINESS SUMMARY")
print("-" * 65)

print(f"Total transactions: {df['Transaction_ID'].nunique():,}")
print(f"Unique customers: {df['Customer_ID'].nunique():,}")
print(f"Unique products: {df['Product'].nunique():,}")
print(f"Total units sold: {df['Quantity'].sum():,.0f}")
print(f"Total revenue: {df['Revenue'].sum():,.2f}")
print(f"Average transaction revenue: {df['Revenue'].mean():,.2f}")

# 2. Sales by product
print("\n2. SALES BY PRODUCT")
print("-" * 65)

product_sales = (
    df.groupby("Product")
    .agg(
        Transactions=("Transaction_ID", "nunique"),
        Units_Sold=("Quantity", "sum"),
        Total_Revenue=("Revenue", "sum"),
        Average_Revenue=("Revenue", "mean"),
    )
    .sort_values("Total_Revenue", ascending=False)
    .round(2)
)

print(product_sales.to_string())

product_sales.to_csv(REPORT_DIR / "sales_by_product.csv")

# 3. Sales by region
print("\n3. SALES BY REGION")
print("-" * 65)

region_sales = (
    df.groupby("Region")
    .agg(
        Transactions=("Transaction_ID", "nunique"),
        Total_Revenue=("Revenue", "sum"),
    )
    .sort_values("Total_Revenue", ascending=False)
    .round(2)
)

print(region_sales.to_string())

region_sales.to_csv(REPORT_DIR / "sales_by_region.csv")

# 4. Sales by payment method
print("\n4. SALES BY PAYMENT METHOD")
print("-" * 65)

payment_sales = (
    df.groupby("Payment_Method")
    .agg(
        Transactions=("Transaction_ID", "nunique"),
        Total_Revenue=("Revenue", "sum"),
    )
    .sort_values("Total_Revenue", ascending=False)
    .round(2)
)

print(payment_sales.to_string())

payment_sales.to_csv(REPORT_DIR / "sales_by_payment_method.csv")

# 5. Monthly sales trend
print("\n5. MONTHLY SALES TREND — FIRST 12 MONTHS")
print("-" * 65)

df["Month"] = df["Date"].dt.to_period("M").astype(str)

monthly_sales = (
    df.groupby("Month")
    .agg(
        Transactions=("Transaction_ID", "nunique"),
        Total_Revenue=("Revenue", "sum"),
    )
    .sort_index()
    .round(2)
)

print(monthly_sales.head(12).to_string())

monthly_sales.to_csv(REPORT_DIR / "monthly_sales.csv")

print("\n" + "=" * 65)
print("ANALYSIS COMPLETE")
print(f"Reports saved in: {REPORT_DIR}")
print("=" * 65)

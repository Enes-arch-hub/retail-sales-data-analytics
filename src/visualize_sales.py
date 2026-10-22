
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "processed" / "retail_sales_clean.csv"
REPORT_DIR = PROJECT_DIR / "reports"
CHART_DIR = REPORT_DIR / "charts"

CHART_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE, parse_dates=["Date"])

print("Creating retail sales charts...")

# 1. Revenue by product
product_sales = (
    df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=True)
)

plt.figure(figsize=(11, 6))
product_sales.plot(kind="barh")
plt.title("Total Revenue by Product")
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.ticklabel_format(axis="x", style="plain")
plt.tight_layout()
plt.savefig(CHART_DIR / "revenue_by_product.png", dpi=150)
plt.close()

# 2. Revenue by region
region_sales = (
    df.groupby("Region")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))
region_sales.plot(kind="bar")
plt.title("Total Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Revenue")
plt.ticklabel_format(axis="y", style="plain")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(CHART_DIR / "revenue_by_region.png", dpi=150)
plt.close()

# 3. Monthly revenue trend
df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()

monthly_sales = (
    df.groupby("Month")["Revenue"]
    .sum()
    .sort_index()
)

plt.figure(figsize=(12, 6))
plt.plot(monthly_sales.index, monthly_sales.values)
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.ticklabel_format(axis="y", style="plain")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(CHART_DIR / "monthly_revenue_trend.png", dpi=150)
plt.close()

# 4. Revenue by payment method
payment_sales = (
    df.groupby("Payment_Method")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))
payment_sales.plot(kind="bar")
plt.title("Revenue by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Revenue")
plt.ticklabel_format(axis="y", style="plain")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(CHART_DIR / "revenue_by_payment_method.png", dpi=150)
plt.close()

print("\nAll four charts created successfully.")

for chart in sorted(CHART_DIR.glob("*.png")):
    print(chart.name)

print(f"\nCharts saved in: {CHART_DIR}")


from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
CLEAN_FILE = PROJECT_DIR / "data" / "processed" / "retail_sales_clean.csv"

if not CLEAN_FILE.exists():
    raise FileNotFoundError(f"Cleaned dataset not found: {CLEAN_FILE}")

print("=" * 60)
print("CLEANED DATASET VALIDATION")
print("=" * 60)

df = pd.read_csv(CLEAN_FILE, parse_dates=["Date"])

# 1. Dataset dimensions
print(f"\nRows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

# 2. Missing values
missing_total = int(df.isna().sum().sum())
print(f"\nTotal missing values: {missing_total:,}")

# 3. Duplicate records
duplicate_rows = int(df.duplicated().sum())
duplicate_ids = int(df["Transaction_ID"].duplicated().sum())

print(f"Exact duplicate rows: {duplicate_rows:,}")
print(f"Repeated transaction IDs: {duplicate_ids:,}")

# 4. Invalid values
invalid_quantities = int((df["Quantity"] <= 0).sum())
invalid_prices = int((df["Unit_Price"] <= 0).sum())

print(f"Non-positive quantities: {invalid_quantities:,}")
print(f"Non-positive prices: {invalid_prices:,}")

# 5. Revenue verification
expected_revenue = (df["Quantity"] * df["Unit_Price"]).round(2)
revenue_mismatches = int(
    (df["Revenue"].round(2) != expected_revenue).sum()
)

print(f"Revenue calculation mismatches: {revenue_mismatches:,}")
print(f"Total revenue: {df['Revenue'].sum():,.2f}")

# 6. Date range
print(f"\nEarliest transaction: {df['Date'].min()}")
print(f"Latest transaction: {df['Date'].max()}")

# 7. Final checks
checks = {
    "No missing values": missing_total == 0,
    "No exact duplicate rows": duplicate_rows == 0,
    "No repeated transaction IDs": duplicate_ids == 0,
    "All quantities are positive": invalid_quantities == 0,
    "All prices are positive": invalid_prices == 0,
    "Revenue is correctly calculated": revenue_mismatches == 0,
}

print("\nVALIDATION CHECKS")
for check, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'}: {check}")

if all(checks.values()):
    print("\nSUCCESS: All validation checks passed.")
else:
    print("\nATTENTION: Some validation checks failed.")


from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "raw" / "retail_sales_dirty.csv"
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

print("=" * 60)
print("RETAIL DATA QUALITY AUDIT")
print("=" * 60)

# Load the full dataset for a comprehensive audit.
# This dataset is around 81 MiB on disk, but uses more RAM
# after Pandas loads it. If memory is limited, we'll switch
# to a chunked audit.
df = pd.read_csv(DATA_FILE)

print(f"\nRows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / (1024**2):.2f} MiB")

# 1. Missing values
missing = pd.DataFrame({
    "Missing_Count": df.isna().sum(),
    "Missing_Percent": (df.isna().mean() * 100).round(3),
})

print("\n1. MISSING VALUES")
print(missing.to_string())

# 2. Exact duplicate rows
duplicate_count = int(df.duplicated().sum())

print("\n2. EXACT DUPLICATE ROWS")
print(f"Duplicate rows: {duplicate_count:,}")

# 3. Invalid numeric values
invalid_quantity = int((df["Quantity"] <= 0).sum())
invalid_price = int((df["Unit_Price"] <= 0).sum())

print("\n3. INVALID NUMERIC VALUES")
print(f"Quantity <= 0: {invalid_quantity:,}")
print(f"Unit_Price <= 0: {invalid_price:,}")

# 4. Text consistency checks
print("\n4. TEXT CONSISTENCY")

for column in [
    "Product", "Category", "Region", "Payment_Method"
]:
    values = df[column].dropna().astype("string")
    extra_spaces = int(values.ne(values.str.strip()).sum())
    capitalization_variants = int(
        values.nunique() - values.str.strip().str.casefold().nunique()
    )

    print(f"\n{column}")
    print(f"Distinct raw values: {values.nunique():,}")
    print(f"Values with surrounding spaces: {extra_spaces:,}")
    print(f"Extra case variants (approx.): {capitalization_variants:,}")

# 5. Date validation
parsed_dates = pd.to_datetime(df["Date"], errors="coerce")
invalid_dates = int(parsed_dates.isna().sum())

print("\n5. DATE VALIDATION")
print(f"Missing or unparseable dates: {invalid_dates:,}")

# 6. Identifier uniqueness
duplicate_transaction_ids = int(
    df["Transaction_ID"].duplicated().sum()
)

print("\n6. IDENTIFIER CHECKS")
print(f"Repeated Transaction_ID values: {duplicate_transaction_ids:,}")

# Save the missing-value report
missing_report = REPORT_DIR / "missing_values_report.csv"
missing.to_csv(missing_report)

print(f"\nMissing-value report saved to: {missing_report}")

print("\nAUDIT COMPLETE — NO DATA HAS BEEN MODIFIED.")

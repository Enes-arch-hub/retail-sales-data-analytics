
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_DIR / "data" / "raw" / "retail_sales_dirty.csv"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
REPORT_DIR = PROJECT_DIR / "reports"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

CLEAN_FILE = PROCESSED_DIR / "retail_sales_clean.csv"
REPORT_FILE = REPORT_DIR / "cleaning_report.txt"

if not RAW_FILE.exists():
    raise FileNotFoundError(f"Raw dataset not found: {RAW_FILE}")

if CLEAN_FILE.exists():
    raise FileExistsError(
        f"{CLEAN_FILE} already exists. Rename or remove it "
        "before running this script again."
    )

# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

print("=" * 60)
print("RETAIL DATA CLEANING")
print("=" * 60)

df = pd.read_csv(RAW_FILE)

original_rows = len(df)
original_columns = len(df.columns)

print(f"\nOriginal rows: {original_rows:,}")
print(f"Original columns: {original_columns}")

# --------------------------------------------------
# 3. REMOVE EXACT DUPLICATES
# --------------------------------------------------

duplicates_removed = int(df.duplicated().sum())
df = df.drop_duplicates().copy()

print(f"\nExact duplicates removed: {duplicates_removed:,}")

# --------------------------------------------------
# 4. STANDARDIZE TEXT
# --------------------------------------------------

text_columns = [
    "Transaction_ID",
    "Customer_ID",
    "Product",
    "Category",
    "Region",
    "Payment_Method",
]

for column in text_columns:
    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
        .replace("", pd.NA)
    )

# Normalize capitalization for categorical fields.
# This preserves readable product and region names.
for column in ["Product", "Category", "Region"]:
    df[column] = df[column].str.title()

df["Payment_Method"] = df["Payment_Method"].str.title()

print("Text columns standardized.")

# --------------------------------------------------
# 5. CONVERT DATA TYPES
# --------------------------------------------------

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")

# --------------------------------------------------
# 6. HANDLE INVALID VALUES
# --------------------------------------------------

# Quantities and unit prices must be positive.
invalid_quantity_rows = int((df["Quantity"] <= 0).sum())
invalid_price_rows = int((df["Unit_Price"] <= 0).sum())

df.loc[df["Quantity"] <= 0, "Quantity"] = pd.NA
df.loc[df["Unit_Price"] <= 0, "Unit_Price"] = pd.NA

print(f"Invalid quantities marked missing: {invalid_quantity_rows:,}")
print(f"Invalid prices marked missing: {invalid_price_rows:,}")

# --------------------------------------------------
# 7. HANDLE MISSING VALUES
# --------------------------------------------------

# Rows without these fields cannot reliably identify a sale
# or calculate its revenue, so remove them.
required_columns = [
    "Transaction_ID",
    "Date",
    "Customer_ID",
    "Product",
    "Quantity",
    "Unit_Price",
    "Region",
    "Payment_Method",
]

before_required_filter = len(df)
df = df.dropna(subset=required_columns).copy()
rows_removed_for_missing_required_data = (
    before_required_filter - len(df)
)

# Category can be recovered from the most common category
# associated with each product.
product_categories = (
    df.dropna(subset=["Product", "Category"])
    .groupby("Product")["Category"]
    .agg(lambda values: values.mode().iloc[0])
    .to_dict()
)

missing_category_before = int(df["Category"].isna().sum())

df["Category"] = df["Category"].fillna(
    df["Product"].map(product_categories)
)

# Use a clear label if the category still cannot be inferred.
df["Category"] = df["Category"].fillna("Unknown")

# --------------------------------------------------
# 8. HANDLE REPEATED TRANSACTION IDS
# --------------------------------------------------

# Keep the first record for each transaction ID.
# This is a conservative rule for this practice dataset;
# real projects should verify the business rules first.
repeated_ids_removed = int(df["Transaction_ID"].duplicated().sum())

df = df.drop_duplicates(
    subset=["Transaction_ID"],
    keep="first",
).copy()

# --------------------------------------------------
# 9. CALCULATE REVENUE
# --------------------------------------------------

df["Revenue"] = (df["Quantity"] * df["Unit_Price"]).round(2)

# --------------------------------------------------
# 10. SAVE CLEANED DATA
# --------------------------------------------------

df.to_csv(CLEAN_FILE, index=False)

# --------------------------------------------------
# 11. CREATE CLEANING REPORT
# --------------------------------------------------

report_lines = [
    "RETAIL DATA CLEANING REPORT",
    "=" * 40,
    f"Original rows: {original_rows:,}",
    f"Original columns: {original_columns}",
    f"Exact duplicate rows removed: {duplicates_removed:,}",
    f"Rows removed for missing required data: "
    f"{rows_removed_for_missing_required_data:,}",
    f"Repeated transaction IDs removed: {repeated_ids_removed:,}",
    f"Invalid quantities identified: {invalid_quantity_rows:,}",
    f"Invalid prices identified: {invalid_price_rows:,}",
    f"Rows remaining: {len(df):,}",
    f"Columns after cleaning: {len(df.columns)}",
    f"Missing values remaining: {int(df.isna().sum().sum()):,}",
    f"Exact duplicates remaining: {int(df.duplicated().sum()):,}",
    f"Repeated transaction IDs remaining: "
    f"{int(df['Transaction_ID'].duplicated().sum()):,}",
    f"Total revenue: {df['Revenue'].sum():,.2f}",
    f"Cleaned dataset: {CLEAN_FILE}",
]

REPORT_FILE.write_text("\n".join(report_lines), encoding="utf-8")

print("\nCLEANING COMPLETE")
print("-" * 60)
print(f"Rows remaining: {len(df):,}")
print(f"Columns remaining: {len(df.columns)}")
print(f"Missing values remaining: {int(df.isna().sum().sum()):,}")
print(f"Exact duplicates remaining: {int(df.duplicated().sum()):,}")
print(f"Cleaned dataset: {CLEAN_FILE}")
print(f"Cleaning report: {REPORT_FILE}")


from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "raw" / "retail_sales_dirty.csv"

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

print("=" * 60)
print("RETAIL DATASET INSPECTION")
print("=" * 60)

# Read only the first 10 rows initially
sample = pd.read_csv(DATA_FILE, nrows=10)

print("\n1. First 10 rows:")
print(sample.to_string(index=False))

print("\n2. Column names:")
print(sample.columns.tolist())

print("\n3. Data types in sample:")
print(sample.dtypes)

print("\n4. File size:")
print(f"{DATA_FILE.stat().st_size / (1024 ** 2):.2f} MiB")

print("\n5. Count all rows in chunks:")
total_rows = 0

for chunk in pd.read_csv(
    DATA_FILE,
    usecols=["Transaction_ID"],
    chunksize=100_000,
):
    total_rows += len(chunk)

print(f"Total rows: {total_rows:,}")

assert total_rows == 1_000_000, "Unexpected row count!"

print("\nPASS: Dataset inspection succeeded.")

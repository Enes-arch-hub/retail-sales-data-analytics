
from pathlib import Path

import numpy as np
import pandas as pd


# -------------------------------------------
# PROJECT CONFIGURATION
# -------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = RAW_DIR / "retail_sales_dirty.csv"

TOTAL_ROWS = 1_000_000
CHUNK_SIZE = 100_000
SEED = 42

PRODUCTS = [
    "Laptop", "Mouse", "Keyboard", "Monitor",
    "Headphones", "Phone", "Tablet", "Charger",
    "USB Cable", "Webcam",
]

CATEGORIES = [
    "Electronics", "Accessories", "Computers",
]

REGIONS = [
    "Nairobi", "Mombasa", "Kisumu",
    "Nakuru", "Eldoret",
]

PAYMENT_METHODS = [
    "Cash", "Card", "Mobile Money", "Bank Transfer",
]


def generate_chunk(
    size: int,
    start_id: int,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate one chunk of deliberately imperfect sales data."""

    customer_numbers = rng.integers(1, 100_001, size=size)

    df = pd.DataFrame({
        "Transaction_ID": [
            f"TXN{i:08d}"
            for i in range(start_id, start_id + size)
        ],
        "Date": pd.to_datetime(
            rng.integers(
                pd.Timestamp("2022-01-01").value // 10**9,
                pd.Timestamp("2026-01-01").value // 10**9,
                size=size,
            ),
            unit="s",
        ).strftime("%Y-%m-%d"),
        "Customer_ID": [
            f"CUST{x:06d}" for x in customer_numbers
        ],
        "Product": rng.choice(PRODUCTS, size=size),
        "Category": rng.choice(CATEGORIES, size=size),
        "Quantity": rng.integers(1, 16, size=size),
        "Unit_Price": np.round(
            rng.uniform(100, 150_000, size=size), 2
        ),
        "Region": rng.choice(REGIONS, size=size),
        "Payment_Method": rng.choice(
            PAYMENT_METHODS, size=size
        ),
    })

    # Problem 1: inconsistent text formatting
    for column in [
        "Product", "Category", "Region", "Payment_Method"
    ]:
        upper_mask = rng.random(size) < 0.08
        df.loc[upper_mask, column] = (
            df.loc[upper_mask, column].str.upper()
        )

        spaces_mask = rng.random(size) < 0.05
        df.loc[spaces_mask, column] = (
            " " + df.loc[spaces_mask, column] + " "
        )

    # Problem 2: missing values
    for column in [
        "Date", "Customer_ID", "Product",
        "Quantity", "Unit_Price", "Region",
    ]:
        missing_mask = rng.random(size) < 0.01
        df.loc[missing_mask, column] = np.nan

    # Problem 3: invalid quantities
    invalid_quantity_mask = rng.random(size) < 0.005
    df.loc[invalid_quantity_mask, "Quantity"] = (
        -rng.integers(1, 6, size=invalid_quantity_mask.sum())
    )

    # Problem 4: invalid prices
    invalid_price_mask = rng.random(size) < 0.005
    df.loc[invalid_price_mask, "Unit_Price"] = (
        -rng.uniform(
            10, 5_000, size=invalid_price_mask.sum()
        ).round(2)
    )

    # Problem 5: exact duplicate records
    # Copy preceding records into selected rows.
    if size > 1:
        duplicate_mask = rng.random(size) < 0.003
        duplicate_indices = np.flatnonzero(duplicate_mask)
        duplicate_indices = duplicate_indices[
            duplicate_indices > 0
        ]

        df.iloc[duplicate_indices] = df.iloc[
            duplicate_indices - 1
        ].to_numpy()

    return df


def main():
    if OUTPUT_FILE.exists():
        raise FileExistsError(
            f"Output already exists: {OUTPUT_FILE}\n"
            "Rename or move the existing file before "
            "generating a new dataset. It will not be "
            "overwritten automatically."
        )

    rng = np.random.default_rng(SEED)
    total_written = 0

    try:
        for start in range(0, TOTAL_ROWS, CHUNK_SIZE):
            current_size = min(
                CHUNK_SIZE, TOTAL_ROWS - start
            )

            chunk = generate_chunk(
                current_size,
                start + 1,
                rng,
            )

            chunk.to_csv(
                OUTPUT_FILE,
                mode="w" if start == 0 else "a",
                header=(start == 0),
                index=False,
            )

            total_written += len(chunk)

            print(
                f"Progress: {total_written:,} "
                f"/ {TOTAL_ROWS:,} rows"
            )

            del chunk

        print("\nDataset generation complete.")
        print(f"Rows generated: {total_written:,}")
        print("Columns: 9")
        print(f"File: {OUTPUT_FILE}")
        print(
            f"File size: "
            f"{OUTPUT_FILE.stat().st_size / (1024**2):.2f} MB"
        )

        assert total_written == TOTAL_ROWS
        print("PASS: Expected row count generated.")

    except Exception:
        if OUTPUT_FILE.exists():
            OUTPUT_FILE.unlink()
        raise


if __name__ == "__main__":
    main()


import pandas as pd
import numpy as np

print("=" * 45)
print("RETAIL DATA CLEANING PROJECT")
print("=" * 45)

# Create a small sample retail dataset
data = {
    "Product": ["Laptop", "Mouse", "Keyboard", "Monitor"],
    "Quantity": [2, 5, 3, 1],
    "Unit_Price": [85000, 1200, 2500, 22000],
}

df = pd.DataFrame(data)

# Calculate revenue for each product
df["Revenue"] = df["Quantity"] * df["Unit_Price"]

print("\nSample retail dataset:")
print(df.to_string(index=False))

# Basic validation tests
assert len(df) == 4
assert df["Revenue"].notna().all()
assert (df["Revenue"] >= 0).all()

print("\nTotal revenue:", f"{df['Revenue'].sum():,}")
print("Number of products:", len(df))
print("All tests passed!")

# Confirm the project can write output files
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent
output_file = project_dir / "reports" / "test_output.csv"

df.to_csv(output_file, index=False)

assert output_file.exists()
print(f"\nTest CSV saved to: {output_file}")

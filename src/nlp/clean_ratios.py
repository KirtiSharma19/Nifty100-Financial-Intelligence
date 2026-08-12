import os

import pandas as pd

# -----------------------------
# Paths
# -----------------------------
INPUT_FILE = "data/raw/financial_ratios.xlsx"
OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "financial_ratios_cleaned.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# Load Excel
# -----------------------------
print("Loading financial_ratios.xlsx...")

df = pd.read_excel(INPUT_FILE)

print(f"Original Rows : {len(df)}")

# -----------------------------
# Remove completely empty rows
# -----------------------------
df = df.dropna(how="all")

# -----------------------------
# Remove duplicate rows
# -----------------------------
df = df.drop_duplicates()

print(f"Rows after duplicate removal : {len(df)}")

# -----------------------------
# Clean Company IDs
# -----------------------------
df["company_id"] = df["company_id"].astype(str).str.strip().str.upper()

# -----------------------------
# Clean Year Column
# -----------------------------
df["year"] = df["year"].astype(str).str.strip()

# -----------------------------
# Convert numeric columns
# -----------------------------
numeric_cols = [
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "return_on_equity_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover",
    "free_cash_flow_cr",
    "capex_cr",
    "earnings_per_share",
    "book_value_per_share",
    "dividend_payout_ratio_pct",
    "total_debt_cr",
    "cash_from_operations_cr",
]

for col in numeric_cols:

    if col in df.columns:

        df[col] = pd.to_numeric(df[col], errors="coerce")

# -----------------------------
# Replace Inf values
# -----------------------------
df = df.replace([float("inf"), float("-inf")], pd.NA)

# -----------------------------
# Sort data
# -----------------------------
df = df.sort_values(by=["company_id", "year"])

# -----------------------------
# Remove duplicate Company-Year
# Keep latest occurrence
# -----------------------------
df = df.drop_duplicates(subset=["company_id", "year"], keep="last")

# -----------------------------
# Fill missing numeric values
# -----------------------------
for col in numeric_cols:

    if col in df.columns:

        df[col] = df.groupby("company_id")[col].transform(lambda x: x.ffill().bfill())

# -----------------------------
# Final reset index
# -----------------------------
df = df.reset_index(drop=True)

# -----------------------------
# Save
# -----------------------------
df.to_csv(OUTPUT_FILE, index=False)

# -----------------------------
# Summary
# -----------------------------
print()

print("Cleaning Completed Successfully")

print("--------------------------------")

print(f"Companies : {df['company_id'].nunique()}")

print(f"Rows      : {len(df)}")

print()

print("Saved To")

print(OUTPUT_FILE)

print()

print(df.head())

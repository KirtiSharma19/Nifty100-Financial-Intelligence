import pandas as pd

from src.services.ratio_engine import DatasetBuilder

# -----------------------------
# Load Data
# -----------------------------

engine = DatasetBuilder()

financial_df = engine.build_dataset()

market_df = pd.read_excel("data/raw/market_cap.xlsx")

# -----------------------------
# Fix Year Column
# -----------------------------

financial_df["year"] = (
    financial_df["year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
    .astype(int)
)

market_df["year"] = market_df["year"].astype(int)

# -----------------------------
# Keep Recent Years
# -----------------------------

financial_df = financial_df[
    financial_df["year"] >= 2019
]

# -----------------------------
# Keep Required Columns
# -----------------------------

market_df = market_df[
    [
        "company_id",
        "year",
        "market_cap_crore",
        "enterprise_value_crore",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "dividend_yield_pct",
    ]
]

# -----------------------------
# Merge
# -----------------------------

merged = financial_df.merge(
    market_df,
    on=["company_id", "year"],
    how="left"
)
# -----------------------------
# Valuation Metrics
# -----------------------------

merged["earnings_yield"] = 100 / merged["pe_ratio"]

merged["book_yield"] = 100 / merged["pb_ratio"]

merged["valuation_score"] = (
    merged["earnings_yield"] +
    merged["book_yield"]
) / 2

# -----------------------------
# Top Valuation Companies
# -----------------------------

top_valuation = (
    merged.sort_values(
        "valuation_score",
        ascending=False
    )
    .head(10)
)

print()
print("=" * 70)
print("TOP 10 VALUATION COMPANIES")
print("=" * 70)

print(
    top_valuation[
        [
            "company_name",
            "year",
            "valuation_score",
            "pe_ratio",
            "pb_ratio",
            "market_cap_crore"
        ]
    ]
)

print("=" * 70)
print("Merged Successfully")
print("=" * 70)

print(merged.head())

print()

print("Rows :", len(merged))

print()

print("Missing Market Cap :", merged["market_cap_crore"].isna().sum())

import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))

plt.bar(
    top_valuation["company_name"],
    top_valuation["valuation_score"]
)

plt.xticks(rotation=45, ha="right")

plt.ylabel("Valuation Score")

plt.title("Top 10 Valuation Companies")

plt.tight_layout()

plt.savefig(
    "exports/charts/valuation_score.png"
)

plt.show()

top_valuation.to_csv(
    "exports/valuation_report.csv",
    index=False
)

print()
print("Valuation Report Saved Successfully")
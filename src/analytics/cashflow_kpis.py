import matplotlib.pyplot as plt

from src.services.ratio_engine import DatasetBuilder

# -----------------------------------
# Load Data
# -----------------------------------

engine = DatasetBuilder()

df = engine.build_dataset()

# -----------------------------------
# Fix Year
# -----------------------------------

df["year"] = df["year"].astype(str).str.extract(r"(\d{4})")[0].astype(int)

# -----------------------------------
# Latest Year
# -----------------------------------

latest_year = df["year"].max()

latest = df[df["year"] == latest_year]

# -----------------------------------
# Select Cash Flow Columns
# -----------------------------------

cashflow = latest[
    [
        "company_name",
        "cash_from_operations_cr",
        "free_cash_flow_cr",
        "capex_cr",
    ]
]

cashflow = cashflow.sort_values("free_cash_flow_cr", ascending=False)

print()
print("=" * 70)
print("TOP CASH FLOW COMPANIES")
print("=" * 70)

print(cashflow.head(10))

# -----------------------------------
# Export Report
# -----------------------------------

cashflow.to_csv("exports/cashflow_report.csv", index=False)

print()
print("Cashflow Report Saved")

# -----------------------------------
# Chart
# -----------------------------------

top = cashflow.head(10)

plt.figure(figsize=(12, 6))

plt.bar(top["company_name"], top["free_cash_flow_cr"])

plt.xticks(rotation=45, ha="right")

plt.ylabel("Free Cash Flow (Cr)")

plt.title("Top 10 Free Cash Flow Companies")

plt.tight_layout()

plt.savefig("exports/charts/cashflow_chart.png")

plt.show()

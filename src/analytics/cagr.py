import pandas as pd

from src.services.ratio_engine import DatasetBuilder

engine = DatasetBuilder()

df = engine.build_dataset()

# -----------------------------
# Convert Year
# -----------------------------

df["year"] = (
    df["year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
    .astype(int)
)

# -----------------------------
# Sales CAGR
# -----------------------------

records = []

for company in df["company_name"].dropna().unique():

    company_df = (
        df[df["company_name"] == company]
        .sort_values("year")
    )

    if len(company_df) < 2:
        continue

    first = company_df.iloc[0]
    last = company_df.iloc[-1]

    start_sales = first["sales"]
    end_sales = last["sales"]

    years = last["year"] - first["year"]

    if years <= 0:
        continue

    if start_sales <= 0:
        continue

    cagr = (
        ((end_sales / start_sales) ** (1 / years)) - 1
    ) * 100

    records.append(
        {
            "company_name": company,
            "start_year": first["year"],
            "end_year": last["year"],
            "sales_cagr": round(cagr, 2)
        }
    )

cagr_df = pd.DataFrame(records)

cagr_df = cagr_df.sort_values(
    "sales_cagr",
    ascending=False
)

print()
print("=" * 70)
print("TOP SALES CAGR COMPANIES")
print("=" * 70)

print(cagr_df.head(10))

cagr_df.to_csv(
    "exports/cagr_report.csv",
    index=False
)

print()
print("CAGR Report Saved")

import matplotlib.pyplot as plt

top = cagr_df.head(10)

plt.figure(figsize=(12,6))

plt.bar(
    top["company_name"],
    top["sales_cagr"]
)

plt.xticks(rotation=45, ha="right")

plt.ylabel("Sales CAGR (%)")

plt.title("Top 10 Sales CAGR Companies")

plt.tight_layout()

plt.savefig(
    "exports/charts/cagr_chart.png"
)

plt.show()
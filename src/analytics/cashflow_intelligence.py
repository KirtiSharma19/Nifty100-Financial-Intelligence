import pandas as pd
import numpy as np
import os
print("=" * 60)
print("Loading Cash Flow Data...")
print("=" * 60)

df = pd.read_excel("data/raw/cashflow.xlsx", header=1)

df = df.rename(columns={
    "Unnamed: 1": "id",
    "Unnamed: 2": "company_id",
    "Unnamed: 3": "year",
    "Unnamed: 4": "operating_activity",
    "Unnamed: 5": "investing_activity",
    "Unnamed: 6": "financing_activity",
    "Unnamed: 7": "net_cash_flow"
})

df = df[
    [
        "id",
        "company_id",
        "year",
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "net_cash_flow",
    ]
]

df = df.dropna(subset=["company_id"])

for col in [
    "operating_activity",
    "investing_activity",
    "financing_activity",
    "net_cash_flow",
]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print(df.head())

df["cfo_quality_score"] = np.where(
    df["operating_activity"] > 0,
    100,
    40
)

df["cfo_quality_label"] = np.where(
    df["operating_activity"] > 0,
    "High Quality",
    "Low Quality"
)

df["capex_intensity_pct"] = (
    abs(df["investing_activity"])
    /
    df["operating_activity"].replace(0, np.nan)
) * 100

df["capex_label"] = np.select(
    [
        df["capex_intensity_pct"] < 3,
        df["capex_intensity_pct"].between(3,8)
    ],
    [
        "Asset Light",
        "Moderate"
    ],
    default="Capital Intensive"
)

df["distress_flag"] = np.where(
    (df["operating_activity"] < 0)
    &
    (df["financing_activity"] > 0),
    "YES",
    "NO"
)

df["deleveraging_flag"] = np.where(
    df["financing_activity"] < 0,
    "YES",
    "NO"
)

df["capital_allocation_label"] = np.select(
    [
        (df["operating_activity"]>0)&(df["investing_activity"]<0),
        (df["operating_activity"]>0)&(df["financing_activity"]<0),
        (df["operating_activity"]<0)
    ],
    [
        "Growth Investment",
        "Debt Reduction",
        "Distress"
    ],
    default="Stable"
)
os.makedirs("output", exist_ok=True)

df.to_excel(
    "output/cashflow_intelligence.xlsx",
    index=False
)

alerts = df[df["distress_flag"]=="YES"]

alerts.to_csv(
    "output/distress_alerts.csv",
    index=False
)

print("="*60)
print("Cash Flow Intelligence Completed")
print("="*60)

print(df.head())

print()

print("Companies :",df["company_id"].nunique())
print("Rows :",len(df))

print()

print("Saved : output/cashflow_intelligence.xlsx")
print("Saved : output/distress_alerts.csv")
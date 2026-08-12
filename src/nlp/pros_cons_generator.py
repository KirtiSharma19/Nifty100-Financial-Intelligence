import os

import pandas as pd

INPUT_FILE = "output/financial_ratios_cleaned.csv"
OUTPUT_FILE = "output/pros_cons_generated.csv"

os.makedirs("output", exist_ok=True)

df = pd.read_csv(INPUT_FILE)

rows = []

for company, grp in df.groupby("company_id"):

    grp = grp.sort_values("year")

    latest = grp.iloc[-1]

    confidence = 60

    # ---------------- PRO RULES ----------------

    if latest["return_on_equity_pct"] >= 20:
        rows.append(
            {
                "company_id": company,
                "type": "Pro",
                "rule_id": "P01",
                "text": "High Return on Equity",
                "confidence_pct": 90,
            }
        )

    if latest["operating_profit_margin_pct"] >= 25:
        rows.append(
            {
                "company_id": company,
                "type": "Pro",
                "rule_id": "P02",
                "text": "Strong Operating Margin",
                "confidence_pct": 85,
            }
        )

    if latest["debt_to_equity"] <= 0.2:
        rows.append(
            {
                "company_id": company,
                "type": "Pro",
                "rule_id": "P03",
                "text": "Very Low Debt",
                "confidence_pct": 88,
            }
        )

    if latest["interest_coverage"] >= 10:
        rows.append(
            {
                "company_id": company,
                "type": "Pro",
                "rule_id": "P04",
                "text": "Excellent Interest Coverage",
                "confidence_pct": 84,
            }
        )

    if latest["cash_from_operations_cr"] > 0:
        rows.append(
            {
                "company_id": company,
                "type": "Pro",
                "rule_id": "P05",
                "text": "Positive Cash From Operations",
                "confidence_pct": 80,
            }
        )

    if latest["free_cash_flow_cr"] > 0:
        rows.append(
            {
                "company_id": company,
                "type": "Pro",
                "rule_id": "P06",
                "text": "Positive Free Cash Flow",
                "confidence_pct": 82,
            }
        )

    # ---------------- CON RULES ----------------

    if latest["return_on_equity_pct"] < 10:
        rows.append(
            {
                "company_id": company,
                "type": "Con",
                "rule_id": "C01",
                "text": "Weak ROE",
                "confidence_pct": 85,
            }
        )

    if latest["operating_profit_margin_pct"] < 10:
        rows.append(
            {
                "company_id": company,
                "type": "Con",
                "rule_id": "C02",
                "text": "Weak Operating Margin",
                "confidence_pct": 84,
            }
        )

    if latest["debt_to_equity"] > 2:
        rows.append(
            {
                "company_id": company,
                "type": "Con",
                "rule_id": "C03",
                "text": "High Debt",
                "confidence_pct": 88,
            }
        )

    if latest["interest_coverage"] < 1.5:
        rows.append(
            {
                "company_id": company,
                "type": "Con",
                "rule_id": "C04",
                "text": "Poor Interest Coverage",
                "confidence_pct": 90,
            }
        )

    if latest["cash_from_operations_cr"] < 0:
        rows.append(
            {
                "company_id": company,
                "type": "Con",
                "rule_id": "C05",
                "text": "Negative Operating Cash Flow",
                "confidence_pct": 86,
            }
        )

    if latest["free_cash_flow_cr"] < 0:
        rows.append(
            {
                "company_id": company,
                "type": "Con",
                "rule_id": "C06",
                "text": "Negative Free Cash Flow",
                "confidence_pct": 88,
            }
        )

result = pd.DataFrame(rows)

result.to_csv(OUTPUT_FILE, index=False)

print("=" * 50)
print("Pros / Cons Generated Successfully")
print("=" * 50)
print(result.head())
print(f"\nTotal Signals : {len(result)}")
print(f"Companies : {result['company_id'].nunique()}")
print(f"Saved : {OUTPUT_FILE}")

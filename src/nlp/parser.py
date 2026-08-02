import re
import pandas as pd

# Read analysis file
df = pd.read_excel("data/raw/analysis.xlsx", skiprows=1)

# Metrics to parse
metrics = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

rows = []

pattern = r"(\d+)\s*Years?:\s*([-\d.]+)%"

for _, row in df.iterrows():

    company = row["company_id"]
    company_row_id = row["id"]

    for metric in metrics:

        value = str(row.get(metric, ""))

        match = re.search(pattern, value)

        if match:

            period = int(match.group(1))
            pct = float(match.group(2))

            rows.append({
                "company_id": company,
                "id": company_row_id,
                "metric_type": metric,
                "period_years": period,
                "value_pct": pct
            })

parsed = pd.DataFrame(rows)

parsed.to_csv(
    "output/analysis_parsed.csv",
    index=False
)

print("Done!")
print(parsed.head())